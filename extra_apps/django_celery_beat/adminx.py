"""Periodic Task Admin interface."""
from __future__ import absolute_import, unicode_literals

from django import forms
from django.conf import settings
from django.forms.widgets import Select
from django.template.defaultfilters import pluralize
from django.utils.translation import ugettext_lazy as _
import xadmin

from celery import current_app
from celery.utils import cached_property
from kombu.utils.json import loads

from .models import (
    PeriodicTask, PeriodicTasks,
    IntervalSchedule, CrontabSchedule,
    SolarSchedule
)
from .utils import is_database_scheduler

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


class IntervalScheduleAdmin(object):
    list_display = ["id", "__str__", "every", "period"]
    list_filter = ["every", "period"]
    search_fields = ["every", "period"]
    model_icon = 'fa fa-calendar-plus-o'
    show_bookmarks = False


class CrontabScheduleAdmin(object):
    model_icon = 'fa fa-clock-o'
    list_display = ["__str__", "minute", "hour", "day_of_week", "day_of_month", "month_of_year"]
    list_filter = ["minute", "hour", "day_of_week", "day_of_month", "month_of_year"]
    search_fields = ["minute", "hour", "day_of_week", "day_of_month", "month_of_year"]
    show_bookmarks = False


class SolarScheduleAdmin(object):
    list_display = ["__str__", "event", "latitude", "longitude"]
    list_filter = ["event", "latitude", "longitude"]
    search_fields = ["event", "latitude", "longitude"]
    model_icon = 'fa fa-sun-o'
    show_bookmarks = False


class TaskSelectWidget(Select):
    """ Widget that lets you choose between task names."""

    celery_app = current_app
    _choices = None

    def tasks_as_choices(self):
        _ = self._modules  # noqa
        tasks = list(sorted(name for name in self.celery_app.tasks
                            if not name.startswith('celery.')))
        return (('', ''), ) + tuple(zip(tasks, tasks))

    @property
    def choices(self):
        if self._choices is None:
            self._choices = self.tasks_as_choices()
        return self._choices

    @choices.setter
    def choices(self, _):
        # ChoiceField.__init__ sets ``self.choices = choices``
        # which would override ours.
        pass

    @cached_property
    def _modules(self):
        self.celery_app.loader.import_default_modules()


class TaskChoiceField(forms.ChoiceField):
    """ Field that lets you choose between task names."""

    widget = TaskSelectWidget

    def valid_value(self, value):
        return True


class PeriodicTaskForm(forms.ModelForm):
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
        exclude = ()

    def clean(self):
        data = super(PeriodicTaskForm, self).clean()
        regtask = data.get('regtask')
        if regtask:
            data['task'] = regtask
        if not data['task']:
            exc = forms.ValidationError(_('Need name of task'))
            self._errors['task'] = self.error_class(exc.messages)
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


class PeriodicTaskAdmin(object):
    """ Admin-interface for periodic tasks."""
    form = PeriodicTaskForm
    model = PeriodicTask
    celery_app = current_app
    """
    name task interval crontab  solar args kwargs queue exchange routing_key expires enabled last_run_at
    total_run_count date_changed description 
    """
    list_display = ['__str__', 'interval', 'crontab',  'queue',
                    'expires', 'enabled', 'last_run_at', 'date_changed']
    list_filter = ['interval', 'crontab', 'expires', 'queue', 'exchange',
                   'routing_key', 'enabled', 'last_run_at', 'date_changed']
    search_fields = ['interval', 'crontab', 'expires', 'queue', 'exchange',
                     'routing_key', 'enabled', 'last_run_at', 'date_changed']
    actions = ('enable_tasks', 'disable_tasks', 'run_tasks')
    fieldsets = (
        (None, {
            'fields': ('name', 'regtask', 'task', 'enabled'),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Schedule', {
            'fields': ('interval', 'crontab', ),
            'classes': ('extrapretty', 'wide', ),
        }),
        ('Arguments', {
            'fields': ('args', 'kwargs'),
            'classes': ('extrapretty', 'wide', 'collapse', 'in'),
        }),
        ('Execution Options', {
            'fields': ('expires', 'queue', 'exchange', 'routing_key'),
            'classes': ('extrapretty', 'wide', 'collapse', 'in'),
        }),
    )

    model_icon = 'fa fa-sitemap'
    show_bookmarks = False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        scheduler = getattr(settings, 'CELERY_BEAT_SCHEDULER', None)
        extra_context['wrong_scheduler'] = not is_database_scheduler(scheduler)
        return super(PeriodicTaskAdmin, self).changelist_view(
            request, extra_context)

    def get_queryset(self, request):
        qs = super(PeriodicTaskAdmin, self).get_queryset(request)
        return qs.select_related('interval', 'crontab')

    def enable_tasks(self, request, queryset):
        rows_updated = queryset.update(enabled=True)
        PeriodicTasks.update_changed()
        self.message_user(
            request,
            _('{0} task{1} {2} successfully enabled').format(
                rows_updated,
                pluralize(rows_updated),
                pluralize(rows_updated, _('was,were')),
            ),
        )
    enable_tasks.short_description = _('Enable selected tasks')

    def disable_tasks(self, request, queryset):
        rows_updated = queryset.update(enabled=False)
        PeriodicTasks.update_changed()
        self.message_user(
            request,
            _('{0} task{1} {2} successfully disabled').format(
                rows_updated,
                pluralize(rows_updated),
                pluralize(rows_updated, _('was,were')),
            ),
        )
    disable_tasks.short_description = _('Disable selected tasks')

    def run_tasks(self, request, queryset):
        self.celery_app.loader.import_default_modules()
        tasks = [(self.celery_app.tasks.get(task.task),
                  loads(task.args),
                  loads(task.kwargs))
                 for task in queryset]
        task_ids = [task.delay(*args, **kwargs)
                    for task, args, kwargs in tasks]
        tasks_run = len(task_ids)
        self.message_user(
            request,
            _('{0} task{1} {2} successfully run').format(
                tasks_run,
                pluralize(tasks_run),
                pluralize(tasks_run, _('was,were')),
            ),
        )
    run_tasks.short_description = _('Run selected tasks')


xadmin.site.register(IntervalSchedule, IntervalScheduleAdmin)
xadmin.site.register(CrontabSchedule, CrontabScheduleAdmin)
xadmin.site.register(PeriodicTask, PeriodicTaskAdmin)


"""
name task interval crontab  solar args kwargs queue exchange routing_key expires enabled last_run_at
total_run_count date_changed description 
"""