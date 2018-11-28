from django.conf.urls import url
from .views import (ClientIndexView, ClientCreateView, ClientOverViewView, ClientStatusView,
                    ClientUpdateView, ClientRemoveView, ProjectListView, SpiderListView, SpiderStartView,
                    JobListView, JobLogView, JobCancelView, ProjectIndexView, ProjectVersionView, ProjectBuildView,
                    ProjectDeployView, ProjectRemoveView, ScheduleView, JobStatusView, DeploymentStatusView)


urlpatterns = [
    url(r'^status$', DeploymentStatusView.as_view(), name="deploy_status"),
    url(r'^client/index/$', ClientIndexView.as_view(), name="client_index"),
    url(r'^client/overview/$', ClientOverViewView.as_view(), name="client_overview"),
    url(r'^client/create/$', ClientCreateView.as_view(), name="client_create"),
    url(r'^client/(\d+)/status/$', ClientStatusView.as_view(), name="client_status"),
    url(r'^client/(\d+)/update/$', ClientUpdateView.as_view(), name="client_update"),
    url(r'^client/(\d+)/remove/$', ClientRemoveView.as_view(), name="client_remove"),
    url(r'^client/(\d+)/schedule/$', ScheduleView.as_view(), name="client_schedule"),
    # url(r'^client/(\d+)/schedule/$', ClientScheduleView.as_view(), name="client_schedule"),
    url(r'^client/(\d+)/projects/$', ProjectListView.as_view(), name="project_list"),
    url(r'^client/(\d+)/project/(\S+)/spiders/$', SpiderListView.as_view(), name="spider_list"),
    url(r'^client/(\d+)/project/(\S+)/spider/(\S+)/$', SpiderStartView.as_view(), name="spider_start"),
    url(r'^client/(\d+)/project/(\S+)/jobs/$', JobListView.as_view(), name="job_list"),

    url(r'^client/(\d+)/project/(\S+)/job/(\S+)/status/$', JobStatusView.as_view(), name="job_status"),

    url(r'^client/(\d+)/project/(\S+)/crawler/(\S+)/job/(\S+)/log/$', JobLogView.as_view(), name="job_log"),
    url(r'^client/(\d+)/project/(\S+)/job/(\S+)/cancel/$', JobCancelView.as_view(), name="job_cancel"),

    url(r'^client/(\d+)/project/(\S+)/version/$', ProjectVersionView.as_view(), name="project_version"),
    url(r'^client/(\d+)/project/(\S+)/deploy/$', ProjectDeployView.as_view(), name="project_client_deploy"),

    url(r'^project/(\S+)/deployment/$', ProjectDeployView.as_view(), name="project_deployment"),
    url(r'^project/index/$', ProjectIndexView.as_view(), name="project_index"),
    url(r'^project/(\S+)/build/$', ProjectBuildView.as_view(), name="project_build"),
    url(r'^project/(\S+)/remove/$', ProjectRemoveView.as_view(), name="project_remove"),
]


