import factory

from . import models as testapps_models


class Sample(factory.django.DjangoModelFactory):
    test_field = "This is test field"
    class Meta:
        model = testapps_models.Sample
