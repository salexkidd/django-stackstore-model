from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StackstoreConfig(AppConfig):
    name = 'stackstore'
    verbose_name = _("Stack store")

