from django.contrib import admin

from stackstore.admin import AbstractStackStoreAdmin

from . import models as testapps_models


@admin.register(testapps_models.Sample)
class Sample(AbstractStackStoreAdmin):
    ...
