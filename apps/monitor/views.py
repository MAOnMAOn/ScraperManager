import os
import logging

from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from utils.paginator import paginator_processing
from utils.mixin_utils import LoginRequireMixin
from .forms import ServerForm, DatabaseClientForm
from .models import Server, DatabaseClient
# from .core.auth import base64_encode, base64_decode
from .core.databases import MysqlClient, MongoClient, RedisClient
from .core.servers import login_server, get_memory, get_cpu_cores, get_cpu_usage, get_top_message

logger = logging.getLogger(__name__)


def save_server_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            servers = Server.objects.all()
            # 进行分页处理
            servers = paginator_processing(request=request, query_set=servers)
            data['html_monitor_list'] = render_to_string('monitor/server_partial_list.html',
                                                         {"servers": servers})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


class ServerIndexView(LoginRequireMixin, View):
    def get(self, request):
        servers = Server.objects.all()
        # 关键词搜索功能
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            try:
                servers = servers.filter(Q(name__icontains=search_keywords) | Q(ip__icontains=search_keywords) |
                                         Q(port=int(search_keywords)) | Q(ssh_user__icontains=search_keywords))
            except ValueError:
                servers = servers.filter(Q(name__icontains=search_keywords) | Q(ip__icontains=search_keywords) |
                                         Q(ssh_user__icontains=search_keywords))
        servers = paginator_processing(request=request, query_set=servers)
        return render(request, "monitor/server_index.html", {"servers": servers})


class ServerPingStatusView(View):
    def get(self, request):
        data = {
            'server_success': 0,
            'server_error': 0,
        }
        servers = Server.objects.all()
        for server in servers:
            response = os.system("ping -c 1 " + str(server.ip))
            if response == 0:
                data['server_success'] += 1
            else:
                data['server_error'] += 1
        return JsonResponse(data)


class ServerStatusView(View):
    def get(self, request, server_id):
        server = get_object_or_404(Server, pk=server_id)
        response = os.system("ping -c 1 " + str(server.ip))
        if response == 0:
            return JsonResponse({'result': '1'})
        else:
            return JsonResponse({'message': 'Connection Error'}, status=500)


class ServerCreateView(View):
    def get(self, request):
        form = ServerForm()
        return save_server_form(request, form, 'monitor/server_create.html')

    def post(self, request):
        form = ServerForm(request.POST)
        return save_server_form(request, form=form, template_name='monitor/server_create.html')


class ServerUpdateView(View):
    def get(self, request, server_id):
        server = get_object_or_404(Server, pk=server_id)
        form = ServerForm(instance=server)
        return save_server_form(request, form, 'monitor/server_update.html')

    def post(self, request, server_id):
        server = get_object_or_404(Server, pk=server_id)
        form = ServerForm(request.POST, instance=server)
        return save_server_form(request, form, 'monitor/server_update.html')


class ServerRemoveView(View):
    def get(self, request, server_id):
        server = get_object_or_404(Server, pk=server_id)
        data = dict()
        context = {'server': server}
        data['html_form'] = render_to_string('monitor/server_delete.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, server_id):
        server = get_object_or_404(Server, pk=server_id)
        data = dict()
        server.delete()
        data['form_is_valid'] = True
        servers = Server.objects.all()
        # 进行分页处理
        servers = paginator_processing(request=request, query_set=servers)
        data['html_monitor_list'] = render_to_string('monitor/server_delete.html',
                                                     {"servers": servers})
        return JsonResponse(data)


class ServerCpuView(View):
    def get(self, request, server_id):
        cpu_info = dict()
        server = get_object_or_404(Server, pk=server_id)
        con = login_server(server.ip, server.port, username=server.ssh_user,
                           password=server.password, rsa_key_file=server.ssh_key_path)
        cpu_info.update(get_cpu_cores(con))
        cpu_info.update(get_cpu_usage(con))
        con.close()
        return JsonResponse(cpu_info)


class ServerMemView(View):
    def get(self, request, server_id):
        server = get_object_or_404(Server, pk=server_id)
        con = login_server(server.ip, server.port, username=server.ssh_user,
                           password=server.password, rsa_key_file=server.ssh_key_path)
        mem_info = get_memory(con)
        con.close()
        return JsonResponse(mem_info)


class ServerTopInfoView(View):
    """ Output top command information """
    def get(self, request, server_id):
        data = dict()
        server = get_object_or_404(Server, pk=server_id)
        try:
            con = login_server(server.ip, server.port, username=server.ssh_user,
                               password=server.password, rsa_key_file=server.ssh_key_path)
            data.update({"name": server.name})
            data.update(get_top_message(con))
            data.update(get_cpu_cores(con))
            data.update(get_memory(con))
            con.close()
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse(data.update({'Error': str(e.args)}), status=500)


def save_database_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            # form.instance.password = base64_encode(request.POST.get('password', '').encode())
            form.save()
            data['form_is_valid'] = True
            databases = DatabaseClient.objects.all()
            # 进行分页处理
            databases = paginator_processing(request=request, query_set=databases)

            data['html_monitor_list'] = render_to_string('monitor/database_partial_list.html',
                                                         {"databases": databases})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


class DatabaseIndexView(LoginRequireMixin, View):
    def get(self, request):
        databases = DatabaseClient.objects.all().order_by('client_type')
        # 关键词搜索功能
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            try:
                if search_keywords == "mysql":
                    search_keywords = 1
                if search_keywords == "mongodb":
                    search_keywords = 2
                if search_keywords == "redis":
                    search_keywords = 3
                databases = databases.filter(Q(client_name__icontains=search_keywords) |
                                             Q(ip__icontains=search_keywords) |
                                             Q(port=int(search_keywords)) | Q(user_name__icontains=search_keywords) |
                                             Q(client_type=int(search_keywords)))
            except ValueError:
                databases = databases.filter(Q(client_name__icontains=search_keywords) |
                                             Q(ip__icontains=search_keywords) | Q(user_name__icontains=search_keywords))
        # 进行分页处理
        databases = paginator_processing(request=request, query_set=databases)
        return render(request, "monitor/database_index.html", {"databases": databases})


class DatabaseStatusView(View):
    def get(self, request, database_id):
        database = get_object_or_404(DatabaseClient, pk=database_id)
        try:
            if database.client_type == 1:
                MysqlClient(host=database.ip, port=database.port,
                            user=database.user_name, password=database.password).show_dbs()
            elif database.client_type == 2:
                res = MongoClient(host=database.ip, port=database.port,
                                  username=database.user_name, password=database.password).show_dbs()
                if not isinstance(res, list):
                    return JsonResponse({'message': res}, status=500)
            elif database.client_type == 3:
                RedisClient(host=database.ip, port=database.port,
                            password=database.password).show_last_db()
            else:
                return JsonResponse({'message': 'Get database type error.'})
            return JsonResponse({'result': '1'})
        except Exception as e:
            return JsonResponse({'message': e.args}, status=500)


class DatabaseClientCreateView(View):
    """ create a database client """
    def get(self, request):
        form = DatabaseClientForm()
        return save_database_form(request, form, 'monitor/database_client_create.html')

    def post(self, request):
        form = DatabaseClientForm(request.POST)
        return save_database_form(request, form=form, template_name='monitor/database_client_create.html')


class DatabaseClientUpdateView(View):
    """ update/edit database client info """
    def get(self, request, database_id):
        database = get_object_or_404(DatabaseClient, pk=database_id)
        form = DatabaseClientForm(instance=database)
        return save_database_form(request, form, 'monitor/database_client_update.html')

    def post(self, request, database_id):
        database = get_object_or_404(DatabaseClient, pk=database_id)
        form = DatabaseClientForm(request.POST, instance=database)
        return save_database_form(request, form, 'monitor/database_client_update.html')


class DatabaseClientRemoveView(View):
    """ remove a database client """
    def get(self, request, database_id):
        database = get_object_or_404(DatabaseClient, pk=database_id)
        data = dict()
        context = {'database': database}
        data['html_form'] = render_to_string('monitor/database_client_delete.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, database_id):
        database = get_object_or_404(DatabaseClient, pk=database_id)
        data = dict()
        database.delete()
        data['form_is_valid'] = True
        databases = DatabaseClient.objects.all()
        # 进行分页处理
        databases = paginator_processing(request=request, query_set=databases)
        data['html_monitor_list'] = render_to_string('monitor/database_partial_list.html',
                                                     {"databases": databases})
        return JsonResponse(data)


class DatabaseDBListView(View):
    def get(self, request, db_client_id, db_type_id):
        db = DatabaseClient.objects.get(id=db_client_id)
        db_overview_list = []
        if str(db_type_id) == "1":
            con = MysqlClient(host=db.ip, port=db.port, user=db.user_name, password=db.password)
            for database in con.show_dbs():
                data_tree = {'text': database, 'tags': [db.client_name, db.client_type],
                             'nodes': [{'text': i, 'href': '/monitor/database/%s/db_type/%s/db/%s/table/%s/'
                                                           % (db.id, db.client_type, database, i)} for i
                                       in con.show_tables(database)]}
                db_overview_list.append(data_tree)
        if str(db_type_id) == "2":
            con = MongoClient(host=db.ip, port=db.port, username=db.user_name, password=db.password)
            for database in con.show_dbs():
                data_tree = {'text': database, 'tags': [db.client_name, db.client_type],
                             'nodes': [{'text': i, 'href': '/monitor/database/%s/db_type/%s/db/%s/table/%s/'
                                                           % (db.id, db.client_type, database, i)} for i in
                                       con.show_collections(database)]}
                db_overview_list.append(data_tree)
        if str(db_type_id) == "3":
            for database in range(16):
                con = RedisClient(host=db.ip, port=db.port, password=db.password, db=database)
                data_tree = {'text': database, 'tags': [db.client_name, db.client_type],
                             'nodes': [{'text': i, 'href': '/monitor/database/%s/db_type/%s/db/%s/table/%s/'
                                                           % (db.id, db.client_type, database, i)} for i
                                       in con.get_keys()]}
                db_overview_list.append(data_tree)
        return JsonResponse(db_overview_list, safe=False)


class DBTableListView(View):
    def get(self, request, db_client_id, db_type_id, database_name, table_name):
        db = DatabaseClient.objects.get(id=db_client_id)
        data = []
        table_info = {'database': database_name}
        if str(db_type_id) == "1":
            con = MysqlClient(host=db.ip, port=db.port, user=db.user_name, password=db.password)
            table_data = con.select_data(db=database_name, table=table_name)
            table_size = con.get_table_size(db=database_name, table=table_name)
            table_info.update({'table': table_name, 'size': table_size, 'db_type': 'mysql'})
            data.append(table_data)
            data.append(table_info)
        if str(db_type_id) == "2":
            con = MongoClient(host=db.ip, port=db.port, username=db.user_name, password=db.password)
            collection_data = con.get_collection_data(db=database_name, collection=table_name)
            collection_size = con.get_collection_size(db=database_name, collection=table_name)
            table_info.update({'collection': table_name, 'size': collection_size, 'db_type': 'mongodb'})
            data.append(collection_data)
            data.append(table_info)
        if str(db_type_id) == "3":
            con = RedisClient(host=db.ip, port=db.port, password=db.password, db=database_name)
            key_data = con.list_members(key=table_name)
            key_size = con.get_key_size(table_name)
            table_info.update({'key': table_name, 'size': key_size, 'db_type': 'redis'})
            data.append(key_data)
            data.append(table_info)
        return JsonResponse(data, safe=False)


"""

"""