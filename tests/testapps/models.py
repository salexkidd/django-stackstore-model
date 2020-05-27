from django.db import models

from stackstore.models import AbstractStackModel


class Sample(AbstractStackModel, models.Model):
    test_field = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
