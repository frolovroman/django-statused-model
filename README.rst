=====
Django Statused Model
=====

Convenient solution of standard tasks for models with statuses.

Project Meaning
-----------
Example of a standard model with status::

    EXAMPLE_STATUSES = [
            ('ready', _('Ready')),
            ('working', _('Working')),
            ('done', _('Done')),
            ('failed', _('Failed')),
        ]

    class ExampleModel(models.Model):
        status = models.CharField(max_length=255, choices=EXAMPLE_STATUSES, default=EXAMPLE_STATUSES[0][0])

In common tasks we forced to use list EXAMPLE_STATUSES with indexes, or it's sting values by themselves.

Variant 1::

    ExampleModel.objects.filter(status=EXAMPLE_STATUSES[0][0])
    if example_instance.status == EXAMPLE_STATUSES[0][0]: ...
    example_instance.status = EXAMPLE_STATUSES[0][0]

Variant 2::

    ExampleModel.objects.filter(status='ready')
    if example_instance.status == 'ready': ...
    example_instance.status = 'ready'

Both this options I don't like. The same case with using module::

    from statused_model import Statuses
    from statused_model.models import StatusedModel, StatusedCharField

    EXAMPLE_STATUSES = Statuses([
            ('ready', _('Ready')),
            ('working', _('Working')),
            ('done', _('Done')),
            ('failed', _('Failed')),
    ])

    class ExampleModel(StatusedModel):
        status = StatusedCharField(max_length=255,
                                   choices=EXAMPLE_STATUSES.choices,
                                   default=EXAMPLE_STATUSES.ready)

    ExampleModel.objects.filter(status=ExampleModel.ready)
    if example_instance.is_ready: ...
    example_instance.set_ready()

1. Excluded the possibility to make typo while specifying the status.
2. You always know what kind of status in the code.
3. You can change the order of statuses without consequences.

Installation
-----------

1. Just add "statused_model" to your INSTALLED_APPS setting.
2. Also for correct working of StatusedModelAdmin you have to add 'django.contrib.staticfiles.finders.AppDirectoriesFinder' to your STATICFILES_FINDERS setting.

Usage
-----------

Statuses
~~~~~~~~~~~~~~~~~~
Optional object which allows you to make the definition of the models more beautiful::

    from statused_model import Statuses

    EXAMPLE_STATUSES = Statuses([
            ('ready', 'Ready'),
            ('working', 'Working'),
            ('done', 'Done'),
            ('failed', 'Failed'),
    ])

    >>> EXAMPLE_STATUSES.working
    'working'

    >>> EXAMPLE_STATUSES[1]
    'working'

    >>> EXAMPLE_STATUSES.list
    ['ready', 'working', 'done', 'failed']

    >>> EXAMPLE_STATUSES.choices
    [('ready', 'Ready'), ('working', 'Working'), ('done', 'Done'), ('failed', 'Failed')]

    >>> EXAMPLE_STATUSES.dict
    {'ready': 'Ready', 'working': 'Working', 'done': 'Done', 'failed': 'Failed'}

    >>> for status in EXAMPLE_STATUSES:
    ...     print(status)
    ...
    ready
    working
    done
    failed

Models
~~~~~~~~~~~~~~~~~~

**Objects:**

1. statused_model.models.StatusedModel
2. statused_model.models.StatusedCharField - replacement of django.models.CharField with additional init argument *status_prefix*
3. statused_model.models.StatusedIntegerField - replacement of django.models.IntegerField with additional init argument *status_prefix*

Back to example::

    from statused_model import Statuses
    from statused_model.models import StatusedModel, StatusedCharField

    EXAMPLE_STATUSES = Statuses([
            ('ready', _('Ready')),
            ('working', _('Working')),
            ('done', _('Done')),
            ('failed', _('Failed')),
    ])

    class ExampleModel(StatusedModel):
        status = StatusedCharField(max_length=255,
                                   choices=EXAMPLE_STATUSES.choices,
                                   default=EXAMPLE_STATUSES.ready)

now ExampleModel class and each it's instance got new attributes:

1. Boolean is_STATUS property comparing status field value with the possible::

    >>> example_instance.status
    'done'
    >>> example_instance.is_ready
    False
    >>> example_instance.is_working
    False
    >>> example_instance.is_done
    True
    >>> example_instance.is_failed
    False

2. Method set_STATUS()::

    >>> example_instance.status
    'done'
    >>> example_instance.set_ready()
    >>> example_instance.status
    'ready'

Note! This method does not store the value in the database!

2. Property same as each status::

    >>> example_instance.ready
    'ready'
    >>> example_instance.working
    'working'
    >>> example_instance.done
    'done'
    >>> example_instance.failed
    'failed'


**Labels:**

If the status contains characters other than numbers and letters, they will be replaced by "_"::

    EXAMPLE_STATUSES = Statuses([
            ('splited status', _('What now?')),
    ])

    >>> example_instance.is_splited_status:
    True

    >>> example_instance.set_splited_status():
    >>> example_instance.status
    'splited status'

**Prefix:**

You can define status fields with *status_prefix* argument. It will be added before status::

    class ExampleModel(StatusedModel):
        status = StatusedCharField(max_length=255, status_prefix="state",
                                   choices=EXAMPLE_STATUSES.choices,
                                   default=EXAMPLE_STATUSES.ready)


    >>> example_instance.is_state_done
    True
    >>> example_instance.set_state_ready()
    >>> example_instance.status
    'ready'
    >>> example_instance.state_done
    'done'

This is allow you to use same status values for different fields.

**None values:**

There is special statuses for values: None and '' - none and empty_string respectively::

    class ExampleModel(StatusedModel):
        status = StatusedCharField(max_length=255,
                                   null=True, blank=True,
                                   choices=EXAMPLE_STATUSES.choices,
                                   default=EXAMPLE_STATUSES.ready)

    >>> example_instance.status
    'done'
    >>> example_instance.set_none()
    >>> type(example_instance.status)
    <class 'NoneType'>
    >>> example_instance.is_none()
    True
    >>> example_instance.set_empty_string()
    >>> example_instance.status
    ''
    >>> example_instance.is_empty_string()
    True

Note! You can't use this strings as your status values!

Admin
~~~~~~~~~~~~~~~~~~
*StatusedModelAdmin* provide additional admin action with status fields changing for multiple instances. Just replace *django.contribadmin.ModelAdmin* with *StatusedModelAdmin*::

    from statused_model import StatusedModelAdmin

    @admin.register(ExampleModel)
    class ExampleModelAdmin(StatusedModelAdmin):
        ...

