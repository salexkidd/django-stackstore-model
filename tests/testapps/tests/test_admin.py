from copy import deepcopy

from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase

from .. import admin as testapps_admin
from .. import factories as testapps_factories
from .. import models as testapps_models


class MockSuperUser:
    def has_perm(self, perm):
        return True


request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockSuperUser()

# If you need to test something using messages
setattr(request, 'session', 'session')
messages = FallbackStorage(request)
setattr(request, '_messages', messages)


class MyAdminTest(TestCase):
    def setUp(self):
        site = AdminSite()
        self.admin = testapps_admin.Sample(testapps_models.Sample, site)

    def test_short_stack_group_uuid(self):
        instance = testapps_factories.Sample()
        self.assertEqual(
            self.admin.short_stack_group_uuid(instance),
            instance.stack_group_uuid.hex[:10]
        )

    def test_only_same_item(self):
        instance = testapps_factories.Sample()
        self.assertIn("a href", self.admin.only_same_item(instance))

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(request))

    def test_delete_model(self):
        instance = testapps_factories.Sample()
        with self.assertRaises(NotImplementedError):
            self.admin.delete_model(request, instance)

    def test_get_queryset(self):
        instance_list = list()

        instance_one = testapps_factories.Sample()
        instance_list.append(deepcopy(instance_one))

        instance_one.save()
        instance_list.append(deepcopy(instance_one))

        instance_two = testapps_factories.Sample()
        instance_list.append(deepcopy(instance_two))

        instance_two.save()
        instance_list.append(deepcopy(instance_two))

        self.assertEqual(instance_list, list(self.admin.get_queryset(request)))

    def test_get_queryset_with_only_latests(self):
        request = request_factory.get('', {'only_latests': "YES"})

        instance_one = testapps_factories.Sample()
        instance_one.save()

        instance_two = testapps_factories.Sample()
        instance_two.save()

        self.assertEqual(
            [instance_one, instance_two],
            list(self.admin.get_queryset(request))
        )
