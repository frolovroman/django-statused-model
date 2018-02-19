from django import forms
from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django.utils.translation import ugettext_lazy as _
from django.forms import modelform_factory


class StatusedModelAdmin(admin.ModelAdmin):
    status_fields = []

    def __init__(self, model, admin_site):
        self.status_fields = model.get_status_fields()
        self.action_form = self.get_action_form()
        super(StatusedModelAdmin, self).__init__(model, admin_site)

    def get_action_form(self):
        form_fields = ActionForm.base_fields.copy()
        for field in self.status_fields:
            widget = forms.Select(attrs={"class": u"status_action_choices",
                                         "id": u"action_set_{}_choices".format(field.name)})
            form_fields.update({u"set_statusfield_" + field.name: field.formfield(required=False, widget=widget)})
        return type('BaseActionForm', (forms.BaseForm,), {'base_fields': form_fields})

    def set_status(self, modeladmin, request, queryset):
        action = request.POST.get('action')
        status = request.POST.get(action) or None
        field = action.split("set_statusfield_")[1]
        for instance in queryset:
            setattr(instance, field, status)
            instance.save(update_fields=[field, ])

    def get_actions(self, request):
        actions = super(StatusedModelAdmin, self).get_actions(request)
        for field in self.status_fields:
            name = field.verbose_name or field.name
            short_description = _("Change {field}").format(field=name)
            name = u"set_statusfield_" + field.name
            actions[name] = (self.set_status, name, short_description)
        return actions

    class Media:
        js = ['statused_model/action_status.js']
