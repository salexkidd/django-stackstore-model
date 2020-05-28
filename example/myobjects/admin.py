from django.contrib import admin

from stackstore.admin import AbstractStackStoreAdmin

from . import models as myobjects_models


@admin.register(myobjects_models.MySampleModel)
class MySampleAdmin(AbstractStackStoreAdmin):
    list_display = (
        "id",
        "title",
        "stack_group_uuid",
        "only_same_item",

    )

    list_display_links = (
        "id",
        "title",
    )
