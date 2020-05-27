import uuid

from django.db import models as django_models


class StackStoreQuerySet(django_models.QuerySet):
    def delete(self):
        raise NotImplementedError(
            "delete method is not available. Use force_delete instead."
        )

    def force_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def latest_from_stack_group(self, *args, **kwargs):
        latest_pk_list = self.values("stack_group_uuid").annotate(
            pk=django_models.Max("pk")
        ).order_by("pk").values_list("pk", flat=True)

        return self.filter(pk__in=latest_pk_list).filter(*args, **kwargs)


class StackManager(django_models.Manager):
    def get_queryset(self, *args, **kwargs):
        return StackStoreQuerySet(self.model)

    def latest_from_stack_group(self, *args, **kwargs):
        return self.get_queryset().latest_from_stack_group(*args, **kwargs)

    def get_latest_from_stack_group(self, *args, **kwargs):
        return self.get_queryset().latest_from_stack_group().get(*args, **kwargs)


class AbstractStackModel(django_models.Model):
    stack_group_uuid = django_models.UUIDField(
        primary_key=False,
        db_index=True,
        unique=False,
        default=uuid.uuid4,
        editable=False,
    )

    def has_pk_and_stack_group_uuid(func):
        def wrapper(self, *args, **kwargs):
            if not self.pk or not self.stack_group_uuid:
                raise self._meta.model.DoesNotExist()

            try:
                return func(self, *args, **kwargs)
            except IndexError as e:
                raise self._meta.model.DoesNotExist()

        return wrapper

    @has_pk_and_stack_group_uuid
    def previous_instance(self):
        return self._meta.model.objects.filter(
            stack_group_uuid=self.stack_group_uuid
        ).filter(pk__lt=self.pk).order_by("-pk")[0]

    @has_pk_and_stack_group_uuid
    def next_instance(self):
        return self._meta.model.objects.filter(
            stack_group_uuid=self.stack_group_uuid).filter(
                pk__gt=self.pk).order_by("pk")[0]

    @has_pk_and_stack_group_uuid
    def latest_instance(self):
        return self._meta.model.objects.filter(
            stack_group_uuid=self.stack_group_uuid).order_by("-pk")[0]

    @has_pk_and_stack_group_uuid
    def earliest_instance(self):
        return self._meta.model.objects.filter(
            stack_group_uuid=self.stack_group_uuid).order_by("pk")[0]

    @has_pk_and_stack_group_uuid
    def same_group_items(self):
        return self._meta.model.objects.filter(
            stack_group_uuid=self.stack_group_uuid)

    def delete(self):
        raise NotImplementedError(
            "delete method is unavailable. please use 'force_delete' method."
        )

    def force_delete(self):
        super().delete()

    def save(self, *args, **kwargs):
        if self.pk and kwargs.pop("__create_new_version", True):
            self.pk = None

        super().save(*args, **kwargs)
        self.refresh_from_db()

    objects = StackManager()

    class Meta:
        abstract = True
        get_latest_by = "pk"
        ordering = ['pk']
