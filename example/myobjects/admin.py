from django.contrib import admin

from stackstore.admin import AbstractStackStoreAdmin

from . import models as myobjects_models


@admin.register(myobjects_models.MySampleModel)
class MySampleAdmin(AbstractStackStoreAdmin):
    ...
