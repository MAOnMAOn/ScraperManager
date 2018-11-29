# -*- coding:utf-8 _*-  

""" 
@author: maonmaon 
@time: 2018/10/18
@contact: 958093654@qq.com
""" 

from __future__ import absolute_import

import os
import json
from itertools import count

import requests
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


from deployment.models import Client
from monitor.core.databases import MysqlClient, MongoClient, RedisClient
from monitor.models import DatabaseClient, Server
from deployment.core.deploy_utils import get_scrapyd, scrapyd_url


@shared_task
def start_spider_job(client, project, spider):
    client = Client.objects.get(name=client)
    scrapyd = get_scrapyd(client)
    scrapyd.schedule(project=project, spider=spider)
    return "success"


def request_scrapyd_client(client, max_reties):
    for retries in count(0):
        try:
            requests.get(scrapyd_url(client.ip, client.port), timeout=3)
            return {"Info": "client %s: request successfully." % (str(client.ip) + ":" + str(client.port))}
        except Exception:
            if retries >= int(max_reties):
                break
            return {"Error": "client %s: request failed." % (str(client.ip) + ":" + str(client.port))}


@shared_task
def check_scrapyd_client(is_send_email, max_reties=3):
    data = dict()
    clients = Client.objects.all()
    for client in clients:
        message = request_scrapyd_client(client, max_reties)
        data.update({client.name: message})
    if is_send_email:
        email_title = "Request scrapyd client"
        email_body = json.dumps(data, indent=2, ensure_ascii=False)
        send_mail(email_title, email_body, settings.DEFAULT_FROM_EMAIL, ["lvyp@idx365.com"])


def ping_server(server, max_reties):
    for retries in count(0):
        response = os.system("ping -c 3 " + str(server.ip))
        if response == 0:
            return {"info": "server %s: ping successfully." % str(server.ip)}
        else:
            if retries >= int(max_reties):
                break
            return {"Error": "sever %s: is down." % str(server.ip)}


@shared_task
def check_server(is_send_email, max_reties=3):
    data = dict()
    servers = Server.objects.all()
    for server in servers:
        message = ping_server(server, max_reties)
        data.update({server.name: message})
    if is_send_email:
        email_title = "Ping Server results"
        email_body = json.dumps(data, indent=2, ensure_ascii=False)
        send_mail(email_title, email_body, settings.DEFAULT_FROM_EMAIL, ["lvyp@idx365.com"])


def test_db_connect(database, max_reties):
    for retries in count(0):
        try:
            if database.client_type == 1:
                MysqlClient(host=database.ip, port=database.port,
                            user=database.user_name, password=database.password).show_dbs()
            elif database.client_type == 2:
                res = MongoClient(host=database.ip, port=database.port,
                                  username=database.user_name, password=database.password).show_dbs()
                if not isinstance(res, list):
                    raise Exception("Mongodb Connect Error.")
            elif database.client_type == 3:
                RedisClient(host=database.ip, port=database.port,
                            password=database.password).show_last_db()
            else:
                return {"Error": "Get database type failed."}
            return {"Info": "Database connected successfully."}
        except Exception as e:
            if retries >= int(max_reties):
                break
            return {"Error": e.args}


@shared_task
def check_database(is_send_email, max_reties=3):
    data = dict()
    databases = DatabaseClient.objects.all()
    for database in databases:
        message = test_db_connect(database=database, max_reties=max_reties)
        data.update({database.client_name: message})
    if is_send_email:
        email_title = "Check Database Status"
        email_body = json.dumps(data, indent=2, ensure_ascii=False)
        send_mail(email_title, email_body, settings.DEFAULT_FROM_EMAIL, ["lvyp@idx365.com"])
