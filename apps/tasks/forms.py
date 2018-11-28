# -*- coding:utf-8 _*-  

""" 
@author: maonmaon 
@time: 2018/10/17
@contact: 958093654@qq.com
"""

from kombu.utils.json import loads
from django import forms
from django.utils.translation import ugettext_lazy as _

from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from django_celery_beat.adminx import TaskChoiceField


class IntervalForm(forms.ModelForm):
    class Meta:
        model = IntervalSchedule
        fields = ('every', 'period', )


class CrontabForm(forms.ModelForm):
    class Meta:
        model = CrontabSchedule
        fields = ('minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year', )


class TaskForm(forms.ModelForm):
    """Form that lets you create and modify periodic tasks."""

    regtask = TaskChoiceField(
        label=_('Task (registered)'),
        required=False,
    )
    task = forms.CharField(
        label=_('Task (custom)'),
        required=False,
        max_length=200,
    )

    class Meta:
        """Form metadata."""
        model = PeriodicTask
        fields = ('name', 'task', 'interval', 'crontab', 'enabled', 'expires', )
        exclude = ()

    def clean(self):
        data = super(TaskForm, self).clean()
        regtask = data.get('regtask')
        if regtask:
            data['task'] = regtask
        if not data['task']:
            exc = forms.ValidationError(_('Need name of task'))
            self._errors['task'] = self.error_class(exc.messages)
            raise exc
        # 我自己加上去的....
        interval_value = self.cleaned_data['interval']
        cron_value = self.cleaned_data['crontab']
        if interval_value is not None and cron_value is not None:
            exc = forms.ValidationError(
                _('Use one of interval/crontab')
            )
            self._errors['interval'] = self.error_class(exc.messages)
            raise exc
        return data

    def _clean_json(self, field):
        value = self.cleaned_data[field]
        try:
            loads(value)
        except ValueError as exc:
            raise forms.ValidationError(
                _('Unable to parse JSON: %s') % exc,
            )
        return value

    def clean_args(self):
        return self._clean_json('args')

    def clean_kwargs(self):
        return self._clean_json('kwargs')

