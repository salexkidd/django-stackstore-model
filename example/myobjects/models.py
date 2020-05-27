from django.db import models

from stackstore.models import AbstractStackModel


class MySampleModel(AbstractStackModel):
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )

    body = models.TextField(
        max_length=1000,
        null=False,
        blank=False,
    )
