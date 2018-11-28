import xadmin

from .models import Client, Project, Deploy


class ClientAdmin(object):
    list_display = ["name", "ip", "port", "created_at", "updated_at"]
    list_filter = ["name", "ip", "port", "auth", "created_at", "updated_at"]
    search_fields = ["name", "ip", "port", "auth", "created_at", "updated_at"]
    model_icon = 'fa fa-university'
    show_bookmarks = False


class ProjectAdmin(object):
    list_display = ["name", "clients", "egg", "desc", "built_at"]
    list_filter = ["name", "clients", "egg", "desc", "built_at"]
    search_fields = ["name", "clients", "egg", "desc", "built_at"]
    model_icon = 'fa fa-folder-open'
    show_bookmarks = False


class DeployAdmin(object):
    list_display = ["project", "client",  "desc", "deployed_at"]
    list_filter = ["project", "client",  "desc", "deployed_at"]
    search_fields = ["project", "client", "deployed_at"]
    model_icon = 'fa fa-cloud-upload'
    show_bookmarks = False


xadmin.site.register(Client, ClientAdmin)
xadmin.site.register(Project, ProjectAdmin)
xadmin.site.register(Deploy, DeployAdmin)

