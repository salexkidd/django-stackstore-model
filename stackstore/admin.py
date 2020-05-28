from urllib import parse as urlparse

from django import forms as forms
from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

ONLY_LATESTS_CHOICE_TUPLE = (
    ('YES', _('YES (Latests Only)')),
)


class OnlyLatestForm(forms.Form):
    only_latests = forms.ChoiceField(
        required=False,
        choices=ONLY_LATESTS_CHOICE_TUPLE,
    )


class OnlyLatestsFilter(admin.SimpleListFilter):
    title = _('only latests')
    parameter_name = 'only_latests'

    def queryset(self, request, queryset):
        return queryset

    def lookups(self, request, model_admin):
        return ONLY_LATESTS_CHOICE_TUPLE


class AbstractStackStoreAdmin(admin.ModelAdmin):

    actions = []

    list_filter = (
        OnlyLatestsFilter,
    )

    list_display_links = (
        "stack_group_uuid",
    )

    list_display = (
        "id",
        "stack_group_uuid",
        "only_same_item",
    )

    search_fields = (
        "id",
        "stack_group_uuid",
    )

    def short_stack_group_uuid(self, obj):
        return obj.stack_group_uuid.hex[:10]

    def only_same_item(self, obj):
        url = reverse("admin:{}_{}_changelist".format(obj._meta.app_label, obj._meta.model_name))

        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update({"stack_group_uuid": obj.stack_group_uuid})
        url_parts[4] = urlparse.urlencode(query)
        url = urlparse.urlunparse(url_parts)

        return format_html('<a href="{}">only same item</a>'.format(url))

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qset = super().get_queryset(request)
        only_latests_form = OnlyLatestForm(request.GET)

        if only_latests_form.is_valid():
            if only_latests_form.cleaned_data["only_latests"] == "YES":
                qset = qset.latest_from_stack_group()

        return qset
