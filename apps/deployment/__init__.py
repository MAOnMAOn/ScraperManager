default_app_config = "deployment.apps.DeploymentConfig"


"""
class ClientScheduleView(View):
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
            return render(request, "deploy/client_schedule.html", {"projects": spider_projects, "client": client})
        except ConnectionError:
            return render(request, "deploy/client_schedule.html", {})


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
                    if status != 'pending':
                        job['start_time'] = job['start_time'].split('.')[0]
                    if status == 'finished':
                        job['end_time'] = job['end_time'].split('.')[0]
                    job['html_spider_job'] = render_to_string('deploy/client_job_list.html', {
                        'client': client, 'project_key': project_name,
                    })
                    jobs.append(job)
            return JsonResponse(jobs, safe=False)
        except ConnectionError:
            return JsonResponse({'message': 'Connect Error'}, status=500)
            

class JobLogView(View):
    def get(self, request, client_id, project_name, spider_name, job_id):
        client = Client.objects.get(id=client_id)
        # get log url
        url = log_url(client.ip, client.port, project_name, spider_name, job_id)
        log_info = dict()
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
            wb_list = [i[20:] for i in text.split('\n') if re.search("scrapy.extensions.logstats.*Crawled", i)]
            for item in wb_list:
                item = re.findall('[1-9]\d*\.\d*|0\.\d*[1-9]\d*$|[0-9]+', item)
                if len(item) > 3:
                    log_info.update({
                        "pages": float(item[0]), "page/min": float(item[1]),
                        "items": float(item[2]), "items/min": float(item[3])
                    })
            log_info.update({"log": text})
            return JsonResponse(log_info)
        except requests.ConnectionError:
            return JsonResponse({'message': 'Load Log Error'}, status=500)
"""