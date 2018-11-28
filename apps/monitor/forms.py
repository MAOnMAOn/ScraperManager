from django import forms

from .models import Server, DatabaseClient


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ('name', 'ip', 'port', 'ssh_user', 'password', 'desc', )


class DatabaseClientForm(forms.ModelForm):
    class Meta:
        model = DatabaseClient
        fields = ('client_name', 'ip', 'port', 'user_name', 'password', 'client_type', 'desc', )

