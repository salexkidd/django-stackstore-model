from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from copy import deepcopy

from .. import models as testapps_models
from .. import factories as testapps_factories


class StackStoreManagerTest(TestCase):
    def test_delete(self):
        with self.assertRaises(NotImplementedError):
            testapps_models.Sample.objects.all().delete()

    def test_force_delete(self):
        instance = testapps_factories.Sample()
        testapps_models.Sample.objects.all().force_delete()
        self.assertNotIn(instance, testapps_models.Sample.objects.all())

    def test_latest_from_stack_group(self):
        instance_one = testapps_factories.Sample()
        instance_two = testapps_factories.Sample()

        for i in range(3):
            instance_one.save()
            instance_two.save()

        queryset = testapps_models.Sample.objects.latest_from_stack_group()
        self.assertEqual(queryset.count(), 2)

        self.assertIn(
            testapps_models.Sample.objects.filter(stack_group_uuid=instance_one.stack_group_uuid).latest(),
            queryset.filter(stack_group_uuid=instance_one.stack_group_uuid)
        )

    def test_get_latest_from_stack_group(self, *args, **kwargs):
        instance_one = testapps_factories.Sample()
        instance_two = testapps_factories.Sample()

        for i in range(3):
            instance_one.save()
            instance_two.save()

        instance_one_latest = testapps_models.Sample.objects.get_latest_from_stack_group(
            stack_group_uuid=instance_one.stack_group_uuid
        )

        self.assertEqual(
            instance_one_latest,
            testapps_models.Sample.objects.filter(stack_group_uuid=instance_one.stack_group_uuid).latest(),
        )


class StackStoreModelTest(TestCase):
    def test_save(self):
        instance = testapps_factories.Sample()
        original_pk = instance.pk

        instance.test_field = "That is test field"
        instance.save()
        instance.refresh_from_db()

        self.assertNotEqual(original_pk, instance.pk)

    def test_save_with_create_new_version_is_false(self):
        instance = testapps_factories.Sample()
        original_pk = instance.pk

        instance.test_field = "That is test field"
        instance.save(__create_new_version=False)

        self.assertEqual(original_pk, instance.pk)

    def test_delete(self):
        instance = testapps_factories.Sample()
        with self.assertRaises(NotImplementedError):
            instance.delete()

    def test_force_delete(self):
        instance = testapps_factories.Sample()
        pk = instance.pk
        instance.force_delete()

        with self.assertRaises(testapps_models.Sample.DoesNotExist):
            testapps_models.Sample.objects.get(pk=pk)

    def test_previous_instance(self):
        instance_one = testapps_factories.Sample()
        instance_one.save()

        _ = testapps_factories.Sample()

        self.assertEqual(
            testapps_models.Sample.objects.filter(stack_group_uuid=instance_one.stack_group_uuid).order_by("pk")[0],
            instance_one.previous_instance()
        )

    def test_previous_instance_if_not_exist(self):
        instance_one = testapps_factories.Sample()
        with self.assertRaises(testapps_models.Sample.DoesNotExist):
            instance_one.previous_instance()

    def test_next_instance(self):
        instance_one = testapps_factories.Sample()
        instance_one_gen_one = deepcopy(instance_one)
        instance_one.save()

        _ = testapps_factories.Sample()

        self.assertEqual(instance_one_gen_one.stack_group_uuid, instance_one.stack_group_uuid)
        self.assertEqual(
            testapps_models.Sample.objects.filter(stack_group_uuid=instance_one_gen_one.stack_group_uuid).order_by("-pk")[0],
            instance_one_gen_one.next_instance()
        )

    def test_next_instance_if_not_exist(self):
        instance_one = testapps_factories.Sample()
        with self.assertRaises(testapps_models.Sample.DoesNotExist):
            instance_one.next_instance()

    def test_latest_instance(self):
        instance_one = testapps_factories.Sample()
        instance_one_gen_one = deepcopy(instance_one)

        _ = testapps_factories.Sample()

        for i in range(3):
            instance_one.save()

        self.assertEqual(
            instance_one_gen_one.latest_instance(),
            instance_one
        )

    def test_earliest_instance(self):
        instance_one = testapps_factories.Sample()
        instance_one_gen_one = deepcopy(instance_one)

        _ = testapps_factories.Sample()

        for i in range(3):
            instance_one.save()

        self.assertEqual(
            instance_one.earliest_instance(),
            instance_one_gen_one
        )

    def test_same_group_items(self):
        instance_list = list()
        instance_one = testapps_factories.Sample()
        instance_list.append(deepcopy(instance_one))

        for i in range(9):
            instance_one.save()
            instance_list.append(deepcopy(instance_one))
        instance_list

        self.assertEqual(instance_list, list(instance_one.same_group_items()))

    def test_has_pk_and_stack_group_uuid_if_pk_is_none(self):
        test_instance = testapps_models.Sample()

        with self.assertRaises(testapps_models.Sample.DoesNotExist):
            self.assertIsNone(test_instance.previous_instance())

        with self.assertRaises(testapps_models.Sample.DoesNotExist):
            self.assertIsNone(test_instance.next_instance())

        with self.assertRaises(testapps_models.Sample.DoesNotExist):
            self.assertIsNone(test_instance.latest_instance())

        with self.assertRaises(testapps_models.Sample.DoesNotExist):
            self.assertIsNone(test_instance.earliest_instance())
