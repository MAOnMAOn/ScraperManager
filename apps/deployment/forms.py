from django import forms

from .models import Client, Deploy


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'ip', 'port', 'desc', )


class DeployForm(forms.ModelForm):

    class Meta:
        model = Deploy
        fields = ('client', 'project', )

    # def __init__(self, *args, **kwargs):
    #     super(DeployForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['project'].queryset = Project.objects.filter(
    #         id__in=Deploy.objects.values_list('project', flat=True).distinct())
