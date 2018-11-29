import os
import re
import time
import datetime

from shutil import rmtree
from os.path import join, exists

import pytz
import requests
from requests.exceptions import ConnectionError

from django.db.models import Q
from django.utils import timezone
from django.views.generic import View
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from ScraperManager.settings import PROJECTS_FOLDER, TIME_ZONE, DATE_TIME_FORMAT

from .forms import ClientForm
from .models import Client, Project, Deploy
from .core.build import build_project, find_egg
from .core.response import JsonResponse as MyJsonResponse
from utils.mixin_utils import LoginRequireMixin
from utils.paginator import paginator_processing
from .core.deploy_utils import (IGNORES, get_traceback, scrapyd_url, log_url, get_scrapyd)


def save_client_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            clients = Client.objects.all().order_by('-id')
            # 进行分页处理
            clients = paginator_processing(request=request, query_set=clients)
            data['html_client_list'] = render_to_string('deploy/client_partial_list.html', {'clients': clients})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


class DeploymentStatusView(View):
    def get(self, request):
        clients = Client.objects.all()
        data = {
            'client_success': 0,
            'client_error': 0,
            'project': 0,
        }
        for client in clients:
            try:
                requests.get(scrapyd_url(client.ip, client.port), timeout=1)
                data['client_success'] += 1
            except ConnectionError:
                data['client_error'] += 1
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        files = os.listdir(path)
        # projects info
        for file in files:
            if os.path.isdir(join(path, file)) and file not in IGNORES:
                data['project'] += 1
        return JsonResponse(data)


class ClientIndexView(LoginRequireMixin, View):
    """ get client list """
    def get(self, request):
        clients = Client.objects.order_by('-id')
        # 关键词搜索功能
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            if re.search('^true$|^t$|^tr$|^tru$|^rue$|^ue$', str(search_keywords), re.IGNORECASE):
                search_keywords = True
            elif re.search('^f$|^fa$|^fal$|^fals$|^false$|^alse$|^lse$|^se$', str(search_keywords), re.IGNORECASE):
                search_keywords = False
            try:
                clients = clients.filter(Q(name__icontains=search_keywords) |
                                         Q(ip__icontains=search_keywords) | Q(port=int(search_keywords)) |
                                         Q(id=int(search_keywords)) | Q(auth=search_keywords))
            except ValueError:
                clients = clients.filter(Q(name__icontains=search_keywords) | Q(ip__icontains=search_keywords))
            except ValidationError:
                clients = clients.filter(Q(name__icontains=search_keywords) |
                                         Q(ip__icontains=search_keywords) | Q(port=int(search_keywords)) |
                                         Q(id=int(search_keywords)))
        clients = paginator_processing(request=request, query_set=clients)
        return render(request, "deploy/client_index.html", {"clients": clients})


class ClientOverViewView(View):
    """ get client list and return json """
    def get(self, request):
        clients = Client.objects.order_by('-id')
        return HttpResponse(serialize('json', clients))


class ClientInfoView(View):
    def get(self, request, client_id):
        return JsonResponse(model_to_dict(Client.objects.get(id=client_id)))


class ClientStatusView(View):
    """ get client status """
    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        try:
            requests.get(scrapyd_url(client.ip, client.port), timeout=3)
            return JsonResponse({'result': '1'})
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)


class ClientUpdateView(View):
    """ update/edit client info """
    def get(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        form = ClientForm(instance=client)
        return save_client_form(request, form, 'deploy/client_update.html')

    def post(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        form = ClientForm(request.POST, instance=client)
        return save_client_form(request, form, 'deploy/client_update.html')


class ClientCreateView(View):
    """ create a client """
    def get(self, request):
        form = ClientForm()
        return save_client_form(request, form, 'deploy/client_create.html')

    def post(self, request):
        form = ClientForm(request.POST)
        return save_client_form(request, form=form, template_name='deploy/client_create.html')


class ClientRemoveView(View):
    """ remove a client """
    def get(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        data = dict()
        context = {'client': client}
        data['html_form'] = render_to_string('deploy/client_delete.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        data = dict()
        client.delete()
        Deploy.objects.filter(client=client).delete()
        data['form_is_valid'] = True
        clients = Client.objects.all()
        # 进行分页处理
        clients = paginator_processing(request=request, query_set=clients)
        data['html_client_list'] = render_to_string('deploy/client_partial_list.html', {'clients': clients})
        return JsonResponse(data)


class ProjectListView(LoginRequireMixin, View):
    """ project deployed list on one client """
    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        try:
            projects = scrapyd.list_projects()
            return JsonResponse(projects, safe=False)
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)


class ProjectIndexView(LoginRequireMixin, View):
    """ project index list """
    def get(self, request):
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        files = os.listdir(path)
        project_index_list = []
        for file in files:
            if os.path.isdir(join(path, file)) and file not in IGNORES:
                project_index_list.append({'name': file})
        return render(request, "deploy/project_index.html", {"projects": project_index_list})


class ProjectRemoveView(View):
    """ remove project from disk and db """
    def get(self, request, project_name):
        project = Project.objects.get(name=project_name)
        data = dict()
        context = {'project': project}
        data['html_form'] = render_to_string('deploy/project_delete.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, project_name):
        # delete deployments
        data = dict()
        project = Project.objects.get(name=project_name)
        Deploy.objects.filter(project=project).delete()
        # delete project
        data['form_is_valid'] = True
        projects = Project.objects.all()
        data['html_client_list'] = render_to_string('deploy/project_partial_list.html',
                                                    {'projects': projects}, request=request)
        result = Project.objects.filter(name=project_name).delete()
        # get project path
        path = join(os.path.abspath(os.getcwd()), PROJECTS_FOLDER)
        project_path = join(path, project_name)
        # delete project file tree
        if exists(project_path):
            rmtree(project_path)
        data.update({'result': result})
        return JsonResponse(data)


class ProjectVersionView(View):
    """ get project deploy version """
    def get(self, request, client_id, project_name):
        # get client and project model
        client = Client.objects.get(id=client_id)
        project = Project.objects.get(name=project_name)
        scrapyd = get_scrapyd(client)
        now_localtime = getattr(timezone, 'template_localtime', timezone.localtime)
        # if deploy info exists in db, return it
        if Deploy.objects.filter(client=client, project=project):
            deploy = Deploy.objects.get(client=client, project=project)
            #
            deploy.deployed_at = now_localtime(deploy.deployed_at).strftime(DATE_TIME_FORMAT)
        # if deploy info does not exists in db, create deploy info
        else:
            try:
                versions = scrapyd.list_versions(project_name)
            except ConnectionError:
                return JsonResponse({'message': 'Connect Error'}, status=500)
            if len(versions) > 0:
                version = versions[-1]
                deployed_at = timezone.datetime.fromtimestamp(int(version), tz=pytz.timezone(TIME_ZONE))
            else:
                deployed_at = None
            deploy, result = Deploy.objects.update_or_create(client=client, project=project, deployed_at=deployed_at)
        # return deploy json info
        return JsonResponse(model_to_dict(deploy))


class ProjectDeployView(LoginRequireMixin, View):
    """ deploy project operation """
    def get(self, request, project_name):
        clients = Client.objects.order_by('-id')
        project = Project.objects.get(name=project_name)
        # 关键词搜索功能
        search_keywords = request.GET.get("keywords", "")
        try:
            clients = clients.filter(Q(id=int(search_keywords)) | Q(name__icontains=search_keywords) |
                                     Q(ip__icontains=search_keywords) | Q(port=int(search_keywords)) |
                                     Q(deploy__desc__icontains=search_keywords)).distinct()
        except ValueError:
            clients = clients.filter(Q(name__icontains=search_keywords) | Q(ip__icontains=search_keywords) |
                                     Q(deploy__desc__icontains=search_keywords)).distinct()
        for client in clients:
            try:
                deploy = Deploy.objects.get(client_id=client.id, project_id=project.id)
                deploy.deployed_at = deploy.deployed_at.strftime(DATE_TIME_FORMAT)
                if deploy.desc:
                    client.deploy_desc = deploy.desc
                else:
                    client.deploy_desc = ''
                if deploy.deployed_at:
                    client.deployed_at = deploy.deployed_at
                else:
                    client.deployed_at = ''
            except Deploy.DoesNotExist:
                pass
        clients = paginator_processing(request=request, query_set=clients)
        return render(request, 'deploy/project_deploy.html', {
            "project_name": project_name, "clients": clients,
        })

    def post(self, request, client_id, project_name):
        # get project folder
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        project_path = join(path, project_name)
        # find egg file
        egg = find_egg(project_path)
        if not egg:
            return JsonResponse({'message': 'egg not found'}, status=500)
        egg_file = open(join(project_path, egg), 'rb')
        # get client and project model
        client = Client.objects.get(id=client_id)
        project = Project.objects.get(name=project_name)
        # execute deploy operation
        scrapyd = get_scrapyd(client)
        try:
            scrapyd.add_version(project_name, int(time.time()), egg_file.read())
            # update deploy info
            deployed_at = timezone.now()
            Deploy.objects.filter(client=client, project=project).delete()
            deploy, result = Deploy.objects.update_or_create(client=client, project=project,
                                                             deployed_at=deployed_at, desc=project.desc)
            return JsonResponse(model_to_dict(deploy))
        except Exception as e:
            return JsonResponse({'message': get_traceback()}, status=500)


class ProjectBuildView(View):
    """ get build info or execute build operation """
    def get(self, request, project_name):
        # get project folder
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        project_path = join(path, project_name)
        # get build version
        egg = find_egg(project_path)
        # if built, save or update project to db
        if egg:
            built_at = timezone.datetime.fromtimestamp(os.path.getmtime(join(project_path, egg)),
                                                       tz=pytz.timezone(TIME_ZONE))
            if not Project.objects.filter(name=project_name):
                Project(name=project_name, built_at=built_at, egg=egg).save()
                model = Project.objects.get(name=project_name)
            else:
                model = Project.objects.get(name=project_name)
                model.built_at = built_at
                model.egg = egg
                model.save()
        # if not built, just save project name to db
        else:
            if not Project.objects.filter(name=project_name):
                Project(name=project_name).save()
            model = Project.objects.get(name=project_name)
        # transfer model to dict then dumps it to json
        data = model_to_dict(model)

        built_at = data['built_at']
        if built_at:
            data['built_at'] = built_at.strftime(DATE_TIME_FORMAT)

        return MyJsonResponse(data)

    def post(self, request, project_name):
        # get project folder
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        project_path = join(path, project_name)

        description = request.POST.get("description", "")
        build_project(project_name)
        egg = find_egg(project_path)
        if not egg:
            return JsonResponse({'message': 'egg not found'}, status=500)
        # update built_at info
        built_at = timezone.now()
        # if project does not exists in db, create it
        if not Project.objects.filter(name=project_name):
            Project(name=project_name, description=description, built_at=built_at, egg=egg).save()
            model = Project.objects.get(name=project_name)
        # if project exists, update egg, description, built_at info
        else:
            model = Project.objects.get(name=project_name)
            model.built_at = built_at
            model.egg = egg
            model.desc = description
            model.save()
        # transfer model to dict then dumps it to json
        data = model_to_dict(model)
        return MyJsonResponse(data)


class ScheduleView(View):
    @staticmethod
    def get_spider_list(request, scrapyd_service, project):
        spiders = []
        try:
            spiders = scrapyd_service.list_spiders(project)
            spiders = [{'id': index_id + 1, 'name': spider} for index_id, spider in enumerate(spiders)]
            # return spiders
        except Exception:
            pass
        return spiders

    @staticmethod
    def get_job_list(request, scrapyd_service, project):
        jobs = []
        try:
            result = scrapyd_service.list_jobs(project)
            statuses = ['pending', 'running', 'finished']
            for status in statuses:
                for job in result.get(status):
                    job['status'] = status
                    jobs.append(job)
        except Exception:
            pass
        return jobs

    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        try:
            projects = scrapyd.list_projects()
            # get spider and job list
            spider_projects = list()
            for project in projects:
                spiders = self.get_spider_list(request=request, scrapyd_service=scrapyd, project=project)
                jobs = self.get_job_list(request=request, scrapyd_service=scrapyd, project=project)
                project = {project: {"spiders": spiders, "jobs": jobs}}
                spider_projects.append(project)
            # return render(request, "deploy/schedule/schedule.html", {"projects": spider_projects, "client": client})
            return render(request, "deploy/client_schedule.html", {"projects": spider_projects, "client": client})
        except ConnectionError:
            return render(request, "deploy/client_schedule.html", {})


class SpiderListView(View):
    """ get spider list from one client """
    def get(self, request, client_id, project_name):
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        try:
            spiders = scrapyd.list_spiders(project_name)
            spiders = [{"project": project_name, 'name': spider,
                        'id': index_id + 1} for index_id, spider in enumerate(spiders)]
            return JsonResponse(spiders, safe=False)
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)


class SpiderStartView(View):
    def get(self, request, client_id, project_name, spider_name):
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        data = dict()
        try:
            job = scrapyd.schedule(project_name, spider_name)
            data['job'] = job
            data['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # the context should be same as the template spider_name is add by myself
            # get param value of cancel spider and spider log
            data['html_spider_job'] = render_to_string('deploy/client_job_list.html', {
                'client': client, 'project_key': project_name, 'spider_name': spider_name,
                'job_id': data['job'], 'start_time': data['start_time'],
            })
            return JsonResponse(data)
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)


class JobListView(View):
    def get(self, request, client_id, project_name):
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        try:
            result = scrapyd.list_jobs(project_name)
            jobs = []
            statuses = ['pending', 'running', 'finished']
            for status in statuses:
                for job in result.get(status):
                    job['status'] = status
                    job['project'] = project_name
                    # if status != 'pending':
                    job['start_time'] = job['start_time'].split('.')[0]
                    if status == 'finished':
                        job['end_time'] = job['end_time'].split('.')[0]
                    job['html_spider_job'] = render_to_string('deploy/client_job_list.html', {
                        'client': client, 'project_key': project_name,
                        'job_id': job.get('id', ''), 'spider_name': job.get('spider', ''),
                        'start_time': job.get('start_time', ''), 'end_time': job.get('end_time', '')
                    })
                    jobs.append(job)
            jobs.reverse()
            return JsonResponse(jobs, safe=False)
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)


class JobLogView(View):
    def get(self, request, client_id, project_name, spider_name, job_id):
        client = Client.objects.get(id=client_id)
        # get log url
        url = log_url(client.ip, client.port, project_name, spider_name, job_id)
        try:
            # get last 1000 bytes of log
            response = requests.get(url, timeout=5, headers={
                'Range': 'bytes=-1000'
            }, auth=(client.username, client.password) if client.auth else None)
            # change encoding
            response.encoding = response.apparent_encoding
            # log not found
            if response.status_code == 404:
                return JsonResponse({'message': 'Log Not Found'}, status=404)
            text = response.text
            return HttpResponse(text)
        except requests.ConnectionError:
            return JsonResponse({'message': 'Load Log Error'}, status=500)


class JobCancelView(View):
    """ cancel a job """
    def get(self, request, client_id, project_name, job_id):
        client = Client.objects.get(id=client_id)
        try:
            scrapyd = get_scrapyd(client)
            result = scrapyd.cancel(project_name, job_id)
            return JsonResponse(result, safe=False)
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'})


class JobStatusView(View):
    def get(self, request, client_id, project_name, job_id):
        """
        get job list of project from one client
        """
        client = Client.objects.get(id=client_id)
        scrapyd = get_scrapyd(client)
        try:
            result = scrapyd.list_jobs(project_name)
            jobs = []
            statuses = ['pending', 'running', 'finished']
            for status in statuses:
                for job in result.get(status):
                    if job.get(job_id) == status:
                        jobs.append({'id': job_id, 'status': status})
                    # job['status'] = status
                    # jobs.append(job)
            return JsonResponse(jobs, safe=False)
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)


"""
from django.conf import settings
from django.utils import timezone

now_localtime = getattr(timezone, 'template_localtime', timezone.localtime)


def now():
    # Return the current date and time.
    if getattr(settings, 'USE_TZ', False):
        return now_localtime(timezone.now())
    else:
        return timezone.now()
"""
