import re
import json

from django.db.models import Q
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import View
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from django_celery_results.models import TaskResult
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule

from .forms import TaskForm, IntervalForm, CrontabForm
from deployment.models import Client, Project
from utils.paginator import paginator_processing
from utils.mixin_utils import LoginRequireMixin

extend_celery = settings.EXTEND_CELERY


def save_job_form(request, form, client_set, project_set, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            client = request.POST.get('client', '')
            project = request.POST.get('project', '')
            spider = request.POST.get('spider', '')
            form.instance.kwargs = json.dumps({
                "client": client,
                "project": project,
                "spider": spider}, indent=2, ensure_ascii=False)
            form.instance.queue = extend_celery.get('deploy').get('queue')
            form.instance.exchange = extend_celery.get('deploy').get('exchange')
            form.instance.routing_key = extend_celery.get('deploy').get('routing_key')
            form.save()
            data['form_is_valid'] = True
            tasks = PeriodicTask.objects.all()
            # 进行分页处理
            tasks = paginator_processing(request=request, query_set=tasks)
            data['html_task_list'] = render_to_string('tasks/job_partial_list.html',
                                                      {"tasks": tasks})
        else:
            data['form_is_valid'] = False
    client = json.loads(form.instance.kwargs).get('client', '')
    project = json.loads(form.instance.kwargs).get('project', '')
    spider = json.loads(form.instance.kwargs).get('spider', '')
    context = {'form': form, 'client_set': client_set, 'project_set': project_set,
               'client': client, 'project': project, 'spider': spider}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def save_my_task_from(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            is_send_email = request.POST.get('is_send_email', '')
            max_reties = request.POST.get('max_retries', '')
            form.instance.kwargs = json.dumps({
                'is_send_email': is_send_email,
                'max_reties': max_reties,
            })
            form.instance.queue = extend_celery.get('monitor').get('queue')
            form.instance.exchange = extend_celery.get('monitor').get('exchange')
            form.instance.routing_key = extend_celery.get('monitor').get('routing_key')
            form.save()
            data['form_is_valid'] = True
            tasks = PeriodicTask.objects.all()
            # 进行分页处理
            tasks = paginator_processing(request=request, query_set=tasks)
            data['html_task_list'] = render_to_string('tasks/job_partial_list.html',
                                                      {"tasks": tasks})
        else:
            data['form_is_valid'] = False
    max_reties = json.loads(form.instance.kwargs).get('max_reties', '')
    is_send_email = json.loads(form.instance.kwargs).get('is_send_email', '')
    context = {'form': form, 'max_reties': max_reties, 'is_send_email': is_send_email}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


class JobsIndex(LoginRequireMixin, View):
    def get(self, request):
        tasks = PeriodicTask.objects.all()
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            if re.search('^true$|^t$|^tr$|^tru$|^rue$|^ue$', str(search_keywords), re.IGNORECASE):
                search_keywords = True
            elif re.search('^f$|^fa$|^fal$|^fals$|^false$|^alse$|^lse$|^se$', str(search_keywords), re.IGNORECASE):
                search_keywords = False
            try:
                tasks = tasks.filter(Q(name__icontains=search_keywords) | Q(task__icontains=search_keywords) |
                                     Q(kwargs__icontains=search_keywords) | Q(enabled=search_keywords) |
                                     Q(interval__every=int(search_keywords)) |
                                     Q(interval__period__icontains=search_keywords))
            except ValidationError:
                tasks = tasks.filter(Q(name__icontains=search_keywords) | Q(task__icontains=search_keywords) |
                                     Q(kwargs__icontains=search_keywords) |
                                     Q(interval__period__icontains=search_keywords))
            except ValueError:
                tasks = tasks.filter(Q(name__icontains=search_keywords) | Q(task__icontains=search_keywords) |
                                     Q(kwargs__icontains=search_keywords) |
                                     Q(interval__period__icontains=search_keywords))
        tasks = paginator_processing(request=request, query_set=tasks)
        return render(request, 'tasks/job_index.html', {'tasks': tasks})


class JobCreateView(View):
    def get(self, request):
        form = TaskForm()
        client_set = Client.objects.all()
        project_set = Project.objects.all()
        return save_job_form(request, form, client_set, project_set, 'tasks/job_create.html')

    def post(self, request):
        form = TaskForm(request.POST)
        client_set = Client.objects.all()
        project_set = Project.objects.all()
        return save_job_form(request, form=form, client_set=client_set, project_set=project_set,
                             template_name='tasks/job_create.html')


class JobUpdateView(View):
    def get(self, request, job_id):
        job = get_object_or_404(PeriodicTask, pk=job_id)
        client_set = Client.objects.all()
        project_set = Project.objects.all()
        form = TaskForm(instance=job)
        return save_job_form(request, form, client_set, project_set, 'tasks/job_update.html')

    def post(self, request, job_id):
        job = get_object_or_404(PeriodicTask, pk=job_id)
        client_set = Client.objects.all()
        project_set = Project.objects.all()
        form = TaskForm(request.POST, instance=job)
        return save_job_form(request, form, client_set, project_set, 'tasks/job_update.html')


class JobRemoveView(View):
    def get(self, request, task_id):
        task = get_object_or_404(PeriodicTask, pk=task_id)
        data = dict()
        context = {'task': task}
        data['html_form'] = render_to_string('tasks/job_delete.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, task_id):
        task = get_object_or_404(PeriodicTask, pk=task_id)
        data = dict()
        task.delete()
        data['form_is_valid'] = True
        tasks = PeriodicTask.objects.all()
        tasks = paginator_processing(request=request, query_set=tasks)
        data['html_task_list'] = render_to_string('tasks/job_partial_list.html', {"tasks": tasks})
        return JsonResponse(data)


class MyTaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        return save_my_task_from(request, form, 'tasks/my_task_create.html')

    def post(self, request):
        form = TaskForm(request.POST)
        return save_my_task_from(request, form=form, template_name='tasks/my_task_create.html')


class MyTaskUpdate(View):
    def get(self, request, task_id):
        task = get_object_or_404(PeriodicTask, pk=task_id)
        form = TaskForm(instance=task)
        return save_my_task_from(request, form, 'tasks/my_task_update.html')

    def post(self, request, task_id):
        task = get_object_or_404(PeriodicTask, pk=task_id)
        form = TaskForm(request.POST, instance=task)
        return save_my_task_from(request, form=form, template_name='tasks/my_task_update.html')


def save_interval_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            intervals = IntervalSchedule.objects.all()
            # 进行分页处理
            intervals = paginator_processing(request=request, query_set=intervals)
            data['html_task_list'] = render_to_string('tasks/interval_partial_list.html',
                                                      {"intervals": intervals})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


class IntervalIndexView(LoginRequireMixin, View):
    def get(self, request):
        intervals = IntervalSchedule.objects.all()
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            try:
                intervals = intervals.filter(Q(every=int(search_keywords)) | Q(id=int(search_keywords)) |
                                             Q(period__icontains=search_keywords))
            except ValueError:
                intervals = intervals.filter(Q(period__icontains=search_keywords))
        intervals = paginator_processing(request=request, query_set=intervals)
        return render(request, 'tasks/interval_index.html', {'intervals': intervals})


class IntervalCreateView(View):
    def get(self, request):
        form = IntervalForm()
        return save_interval_form(request, form, 'tasks/interval_create.html')

    def post(self, request):
        form = IntervalForm(request.POST)
        return save_interval_form(request, form=form, template_name='tasks/interval_create.html')


class IntervalUpdateView(View):
    def get(self, request, interval_id):
        interval = get_object_or_404(IntervalSchedule, pk=interval_id)
        form = IntervalForm(instance=interval)
        return save_interval_form(request, form, 'tasks/interval_update.html')

    def post(self, request, interval_id):
        interval = get_object_or_404(IntervalSchedule, pk=interval_id)
        form = IntervalForm(request.POST, instance=interval)
        return save_interval_form(request, form, 'tasks/interval_update.html')


class IntervalRemoveView(View):
    def get(self, request, interval_id):
        interval = get_object_or_404(IntervalSchedule, pk=interval_id)
        data = dict()
        context = {'interval': interval}
        data['html_form'] = render_to_string('tasks/interval_delete.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, interval_id):
        interval = get_object_or_404(IntervalSchedule, pk=interval_id)
        data = dict()
        interval.delete()
        data['form_is_valid'] = True
        intervals = IntervalSchedule.objects.all()
        intervals = paginator_processing(request=request, query_set=intervals)
        data['html_task_list'] = render_to_string('tasks/interval_partial_list.html',
                                                  {'intervals': intervals})
        return JsonResponse(data)


def save_crontab_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            crontabs = CrontabSchedule.objects.all()
            # 进行分页处理
            crontabs = paginator_processing(request=request, query_set=crontabs)
            data['html_task_list'] = render_to_string('tasks/crontab_partial_list.html',
                                                      {"crontabs": crontabs})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


class CrontabIndexView(LoginRequireMixin, View):
    def get(self, request):
        crontabs = CrontabSchedule.objects.all()
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            try:
                crontabs = crontabs.filter(Q(id=int(search_keywords)) | Q(minute__icontains=search_keywords) |
                                           Q(hour__icontains=search_keywords) |
                                           Q(day_of_week__icontains=search_keywords) |
                                           Q(day_of_month__icontains=search_keywords) |
                                           Q(month_of_year__icontains=search_keywords))
            except ValueError:
                crontabs = crontabs.filter(Q(minute__icontains=search_keywords) | Q(hour__icontains=search_keywords) |
                                           Q(day_of_week__icontains=search_keywords) |
                                           Q(day_of_month__icontains=search_keywords) |
                                           Q(month_of_year__icontains=search_keywords))
        crontabs = paginator_processing(request=request, query_set=crontabs)
        return render(request, 'tasks/crontab_index.html', {'crontabs': crontabs})


class CrontabCreateView(View):
    def get(self, request):
        form = CrontabForm()
        return save_crontab_form(request, form, 'tasks/crontab_create.html')

    def post(self, request):
        form = CrontabForm(request.POST)
        return save_crontab_form(request, form=form, template_name='tasks/crontab_create.html')


class CrontabUpdateView(View):
    def get(self, request, crontab_id):
        crontab = get_object_or_404(CrontabSchedule, pk=crontab_id)
        form = CrontabForm(instance=crontab)
        return save_crontab_form(request, form, 'tasks/crontab_update.html')

    def post(self, request, crontab_id):
        crontab = get_object_or_404(CrontabSchedule, pk=crontab_id)
        form = CrontabForm(request.POST, instance=crontab)
        return save_crontab_form(request, form, 'tasks/crontab_update.html')


class CrontabRemoveView(View):
    def get(self, request, crontab_id):
        crontab = get_object_or_404(CrontabSchedule, pk=crontab_id)
        data = dict()
        context = {'crontab': crontab}
        data['html_form'] = render_to_string('tasks/crontab_delete.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, crontab_id):
        crontab = get_object_or_404(CrontabSchedule, pk=crontab_id)
        data = dict()
        crontab.delete()
        data['form_is_valid'] = True
        crontabs = CrontabSchedule.objects.all()
        crontabs = paginator_processing(request=request, query_set=crontabs)
        data['html_task_list'] = render_to_string('tasks/crontab_partial_list.html', {'crontabs': crontabs})
        return JsonResponse(data)


class ResultsIndexView(LoginRequireMixin, View):
    def get(self, request):
        results = TaskResult.objects.all()
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            results = results.filter(Q(task_id__icontains=search_keywords) | Q(task_name__icontains=search_keywords) |
                                     Q(task_kwargs__icontains=search_keywords) | Q(result__icontains=search_keywords) |
                                     Q(status__icontains=search_keywords))
        results = paginator_processing(request=request, query_set=results)
        return render(request, 'tasks/results_index.html', {'results': results})


class ResultsRemoveView(View):
    def get(self, request, result_id):
        data = dict()
        result = get_object_or_404(TaskResult, pk=result_id)
        context = {'result': result}
        data['html_form'] = render_to_string('tasks/result_delete.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, result_id):
        data = dict()
        result = get_object_or_404(TaskResult, pk=result_id)
        result.delete()
        data['form_is_valid'] = True
        results = TaskResult.objects.all()
        results = paginator_processing(request=request, query_set=results)
        data['html_task_list'] = render_to_string('tasks/results_partial_list.html', {'results': results})
        return JsonResponse(data)



