# -*- coding:utf-8 _*-  

""" 
@author: maonmaon 
@time: 2018/10/17
@contact: 958093654@qq.com
""" 

from django.conf.urls import url


from .views import (JobsIndex, JobCreateView, JobUpdateView, JobRemoveView, IntervalIndexView,
                    IntervalCreateView, IntervalUpdateView, IntervalRemoveView, CrontabIndexView,
                    CrontabCreateView, CrontabUpdateView, CrontabRemoveView, MyTaskCreateView,
                    MyTaskUpdate, ResultsIndexView, ResultsRemoveView)


urlpatterns = [
    url(r'^job/index/$', JobsIndex.as_view(), name="job_index"),
    url(r'^job/create/$', JobCreateView.as_view(), name="job_create"),
    url(r'^job/(\d+)/update/$', JobUpdateView.as_view(), name="job_update"),
    url(r'^job/(\d+)/remove/$', JobRemoveView.as_view(), name="job_remove"),
    url(r'^my_task/create/$', MyTaskCreateView.as_view(), name="my_task_create"),
    url(r'^my_task/(\d+)/update/$', MyTaskUpdate.as_view(), name="my_task_update"),

    url(r'^interval/index/$', IntervalIndexView.as_view(), name="interval_index"),
    url(r'^interval/create/$', IntervalCreateView.as_view(), name="interval_create"),
    url(r'^interval/(\d+)/update/$', IntervalUpdateView.as_view(), name="interval_update"),
    url(r'^interval/(\d+)/remove/$', IntervalRemoveView.as_view(), name="interval_remove"),
    url(r'^crontab/index/$', CrontabIndexView.as_view(), name="crontab_index"),
    url(r'^crontab/create/$', CrontabCreateView.as_view(), name="crontab_create"),
    url(r'^crontab/(\d+)/update/$', CrontabUpdateView.as_view(), name="crontab_update"),
    url(r'^crontab/(\d+)/remove/$', CrontabRemoveView.as_view(), name="crontab_remove"),
    url(r'^result/index/$', ResultsIndexView.as_view(), name="result_index"),
    url(r'^result/(\d+)/remove/$', ResultsRemoveView.as_view(), name="result_remove"),

]
