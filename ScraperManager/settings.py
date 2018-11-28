"""
Django settings for ScraperManager project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8u)yd=-d0i&z_1fxcm9ifr^f#8+5*5=(878rot8x0a(5kommj5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'xadmin',
    'django_mysql',
    'pure_pagination',
    'deployment',
    'users',
    'monitor',
    'tasks',
    'django_celery_beat',
    'django_celery_results',
    'captcha',
    'widget_tweaks',
]

AUTH_USER_MODEL = "users.UserProfile"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ScraperManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ScraperManager.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'zh-hans'  # 中文支持，django1.8以后支持；1.8以前是zh-cn

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True   # 默认是True，时间是utc时间，由于我们要用本地时间，所用手动修改为false！！！


STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),    # 一定要加逗号
)
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# settings for spider deployment
PROJECTS_FOLDER = os.path.join(BASE_DIR, 'projects')
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


EMAIL_HOST = "smtp.mxhichina.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "lvyp@idx365.com"
EMAIL_HOST_PASSWORD = "Idxmail8"
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CELERYD_CONCURRENCY = 4  # worker 并发数， 相当于--concurrency 参数
# CELERYD_FORCE_EXECV = True  # 防止死锁
CELERY_DISABLE_RATE_LIMITS = True  # 任务发出后，经过一段时间未收到acknowledge, 就把任务交给其他worker执行
CELERYD_MAX_TASKS_PER_CHILD = 60  # 每个worker执行多少个任务就销毁，防止内存泄露, --max tasks per child
CELERYD_PREFETCH_MULTIPLIER = 10  # 每次获取任务的数量
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 43200}
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_COUNT = ['json', 'msgpack']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，默认的时区是UTC

# formatter: 'amqp://user:password@ip:port/vhost'
CELERY_BROKER_URL = 'amqp://slkj:qwertyuiop@192.168.2.53:5672/scraper_manager'
# CELERY_RESULT_BACKEND = 'redis://root:foobared@127.0.0.1:6379/3'

#  celery -A DjangoCelery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# CELERY_BEAT_SCHEDULE_FILENAME = '/tmp/celery-beat-schedule.log'


EXTEND_CELERY = {"deploy": {"exchange": "crawler_deploy_exchange", "queue": "crawler_deploy_queue",
                            "routing_key": "crawler_deploy_routing_key"},
                 "monitor": {"exchange": "crawler_monitor_exchange", "queue": "crawler_monitor_queue",
                             "routing_key": "crawler_monitor_routing_key"},
                 "common": {"exchange": "crawler_common_exchange", "queue": "crawler_common_queue",
                            "routing_key": "crawler_common_routing_key"},
                 "media": {"exchange": "crawler_media_exchange", "queue": "crawler_media_queue",
                           "routing_key": "crawler_media_routing_key"}}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'monitor': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
