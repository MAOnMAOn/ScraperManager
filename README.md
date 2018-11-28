# ScraperManager

基于Scrapy，Scrapyd，Scrapyd-API，Django, Celery的分布式爬虫管理工具. 项目灵感来自于
[Gerapy](https://github.com/Gerapy/Gerapy).

## 安装启动

首先, 请确保安装python3, 推荐使用python3.6版本, 并使用anaconda进行环境管理.

拷贝项目, 进入项目目录, 并安装相应依赖:

```
git clone https://github.com/MAOnMAOn/ScraperManager
cd ScraperManager
pip install -r requirements.txt
```

在项目目录内初始化数据库:

```
python3.6 manage.py migrate
```

创建超级管理员:

```
python3.6 manage.py createsuperuser
```

启动项目:

```
python3.6 manage.py runserver 0.0.0.0:8000
```

现在, 可以在浏览器访问 http://localhost:8000.


## 启用定时任务功能

首先请确保安装rabbitmq, 

```
sudo rabbitmqctl add_user user password  # 创建用户
sudo rabbitmqctl add_vhost scraper_manager  # 创建虚拟机
sudo rabbitmqctl set_permissions -p scraper_manager user ".*" ".*" ".*"
```

如何, 修改项目的settings.py 文件之中celery broker 相关配置, 编辑settings.py文件:

```
# formatter: 'amqp://user:password@ip:port/vhost'
CELERY_BROKER_URL = 'amqp://user:password@localhost:5672/scraper_manager'
```

最后启动celery worker 以及celery beat

```
celery -A ScraperManager beat -l info
celery worker -A ScraperManager -l info
```

也可以考虑使用多重视窗管理工具 screen, 以及通过supervisor 管理celery.

