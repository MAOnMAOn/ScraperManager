# -*- coding:utf-8 _*-  

""" 
@author: maonmaon 
@time: 2018/10/18
@contact: 958093654@qq.com
""" 

from __future__ import absolute_import, unicode_literals

import os
import django

from kombu import Queue, Exchange
from celery import Celery, platforms
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScraperManager.settings')
django.setup()


platforms.C_FORCE_ROOT = False

extend_celery = settings.EXTEND_CELERY
deploy_exchange = Exchange(extend_celery.get('deploy').get('exchange'), type="topic")
monitor_exchange = Exchange(extend_celery.get('monitor').get('exchange'), type="topic")
common_exchange = Exchange(extend_celery.get('common').get('exchange'), type="topic")
media_exchange = Exchange(extend_celery.get('media').get('exchange'), type='topic')

queue = (
    Queue(extend_celery.get('deploy').get('queue'), deploy_exchange,
          routing_key=extend_celery.get('deploy').get('routing_key')),
    Queue(extend_celery.get('monitor').get('queue'), monitor_exchange,
          routing_key=extend_celery.get('monitor').get('routing_key')),
    Queue(extend_celery.get('common').get('queue'), common_exchange,
          routing_key=extend_celery.get('common').get('routing_key')),
    Queue(extend_celery.get('media').get('queue'), media_exchange,
          routing_key=extend_celery.get('media').get('routing_key')),
    Queue('celery', Exchange('celery'), routing_key='celery'),
)

route = {
    'monitor.tasks.start_spider_job': {
        'queue': extend_celery.get('deploy').get('queue'),
        'routing_key': extend_celery.get('deploy').get('routing_key'),
    },
    'monitor.tasks.add3': {
        'queue': 'crawler_monitor_queue',
        'routing_key': 'crawler_monitor_routing_key',
    },
    'monitor.tasks.add': {
        'queue': 'media_crawler_queue',
        'routing_key': 'media_crawler_routing_key',
    },
}

app = Celery('ScraperManager')

# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(CELERY_QUEUES=queue, CELERY_ROUTES=route)

app.loader.override_backends['django-db'] = 'django_celery_results.backends.database:DatabaseBackend'


"""
EXTEND_CELERY = {"deploy": {"exchange": "crawler_deploy_exchange", "queue": "crawler_deploy_queue", 
                            "routing_key": "crawler_deploy_routing_key"}, 
                 "monitor": {"exchange": "crawler_monitor_exchange", "queue": "crawler_monitor_queue", 
                             "routing_key": "crawler_monitor_routing_key"}, 
                 "common": {"exchange": "crawler_common_exchange", "queue": "crawler_common_queue", 
                            "routing_key": "crawler_common_routing_key"}, 
                 "media": {"exchange": "crawler_media_exchange", "queue": "crawler_media_queue", 
                           "routing_key": "crawler_media_routing_key"}}
"""

