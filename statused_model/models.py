import re
from django.db import models
from django.core import checks


class StatusedField(object):
    status_prefix = ''

    def __init__(self, status_prefix='', *args, **kwargs):
        super(StatusedField, self).__init__(*args, **kwargs)
        self.status_prefix = status_prefix


class StatusedCharField(StatusedField, models.CharField):
    pass


class StatusedIntegerField(StatusedField, models.IntegerField):
    pass


class StatusedModel(models.Model):
    _statuses_initialized = False

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        if not self._statuses_initialized:
            self.set_statuses()
            self._statuses_initialized = True
        super(StatusedModel, self).__init__(*args, **kwargs)

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_status_fields(**kwargs))
        return errors

    @classmethod
    def _check_status_fields(cls, **kwargs):
        status_labels = []
        for field in cls.get_status_fields():
            for status, status_name in field.choices:
                status_label = cls.get_status_label(status, field.status_prefix)
                if status_label in status_labels:
                    return [checks.Error('Status "{}" is duplicated.'.format(status_label),
                                         hint='You have to change status_prefix.', obj=cls)]
                status_labels.append(status_label)
        return []

    @classmethod
    def get_status_fields(cls):
        status_fields = []
        for field in cls._meta.get_fields():
            if isinstance(field, StatusedCharField) or isinstance(field, StatusedIntegerField):
                status_fields.append(field)
        return status_fields

    @classmethod
    def set_statuses(cls):
        for field in cls.get_status_fields():
            for status, status_name in field.choices:
                status_label = cls.get_status_label(status, field.status_prefix)
                setattr(cls, 'is_' + status_label,
                        property(lambda obj, obj_status=status: getattr(obj, field.name) == obj_status))
                setattr(cls, 'set_' + status_label,
                        lambda obj, obj_status=status: setattr(obj, field.name, obj_status))
                setattr(cls, status_label, status)

    @staticmethod
    def get_status_label(status, prefix=''):
        status_label = 'none'
        if status:
            status_label = re.sub('[^0-9a-zA-Z]+', '_', status)
        if prefix:
            status_label = prefix + "_" + status_label
        return status_label
