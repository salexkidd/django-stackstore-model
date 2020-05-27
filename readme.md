Django Staskstore model
=========================================================================================

[![CircleCI](https://circleci.com/gh/salexkidd/django-stackstore-model.svg?style=svg)](https://circleci.com/gh/salexkidd/django-stackstore-model)

Djanog Stackstore is a library that can support model versioning in a minimal amount of steps.

- Support Django 2 and 3
- Support Python3.7, 3.8 (Maybe 2.7. Not tested)


# Usage

```
# models.py
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
```

Python shell
```

# Create First version instance
>>> instance = MySampleModel.objects.create(title="Test", body="This is test text")
>>> instance.pk
1

# If you save this instance, create new version instance
>>> instance.title = "Test (version2)"
>>> instance.save()
>>> instance.pk
2

# If you can fetch previous version
>>> previous_instance = instance.previous_instance()
>>> previous_instance.pk
1

# You can get next version
>>> previous_instance.next_instance().pk
2
```


# API

## QuerySet & Manager

### latest_from_stack_group

Returns a QuerySet of the most recent objects in each Stackgroup.

```
# Create instance
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> instance_lunch = MySampleModel.objects.create(title="Today's lunch", body="Spam with Beacon") # Create <MySampleModel: MySampleModel object (2)>

# Save each instance
>>> instance_breakfast.body = "Fried Egg with bread"
>>> instance_breakfast.save() # Save method create new <MySampleModel: MySampleModel object (3)>

>>> instance_lunch.body = "Meat Pasta"
>>> instance_lunch.save() # Save method create new <MySampleModel: MySampleModel object (4)>

>>> MySampleModel.objects.latest_from_stack_group() # You can fetch 3 & 4 My Sample Model
<StackStoreQuerySet [<MySampleModel: MySampleModel object (3)>, <MySampleModel: MySampleModel object (4)>]>

```
### get_latest_from_stack_group

Returns an object that matches the collation parameter from the latest set of objects in each Stackgroup.

```
# Create instance
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> instance_lunch = MySampleModel.objects.create(title="Today's lunch", body="Spam with Beacon") # Create <MySampleModel: MySampleModel object (2)>

# Save each instance
>>> instance_breakfast.body = "Fried Egg with bread"
>>> instance_breakfast.save() # Save method create new <MySampleModel: MySampleModel object (3)>

>>> MySampleModel.objects.get_latest_from_stack_group(body="Fried Egg with bread")
<MySampleModel: MySampleModel object (3)>
```


## model object

### save

When an object is saved, a new object is created and assigned the same stack_group_uuid as the object from which it was saved.
This means that a new version will be generated.

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> instance_breakfast.body = "Fried Egg with bread"
>>> instance_breakfast.save() # Save method create version object <MySampleModel: MySampleModel object (2)>
>>> MySampleModel.objects.all()
<StackStoreQuerySet [<MySampleModel: MySampleModel object (1)>, <MySampleModel: MySampleModel object (2)>]>
```

If you want to save the overwrite without creating a new version, you should pass `False` to `__create_new_version` in the `save` method.

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg")
>>> instance_breakfast.save(__create_new_version=False)
>>> instance_breakfast.pk
1
```

### force_delete

Remove the object.

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> MySampleModel.objects.all()
<StackStoreQuerySet [<MySampleModel: MySampleModel object (1)>]>
>>> instance_breakfast.force_delete()
>>> MySampleModel.objects.all()
<StackStoreQuerySet []>
```

Calling the existing `delete` method will raise a NotImplementedError exception.

### same_group_items

Returns a QuerySet that returns all objects belonging to the same Stackgroup.

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> [instance_breakfast.save() for i in range(2)]
>>> instance_breakfast.same_group_items()
<StackStoreQuerySet [<MySampleModel: MySampleModel object (3)>, <MySampleModel: MySampleModel object (2)>, <MySampleModel: MySampleModel object (1)>]>
```

### previous_instance

Returns the previous version of the object.

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> [instance_breakfast.save() for i in range(2)]
>>> second_gen_instance = instance_breakfast.same_group_items().order_by("pk")[1]
>>> second_gen_instance.previous_instance()
<MySampleModel: MySampleModel object (1)>
```

Throws a DoesNotExist exception if the object does not exist.


### next_instance

Returns the next version of the object.

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> [instance_breakfast.save() for i in range(2)]
>>> second_gen_instance = instance_breakfast.same_group_items()[1]
>>> second_gen_instance.next_instance()
<MySampleModel: MySampleModel object (3)>
```

Throws a DoesNotExist exception if the object does not exist.


### latest_instance

Returns the most recent object of the Stackgroup to which its own object belongs.

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> [instance_breakfast.save() for i in range(2)]
>>> first_gen_instance = instance_breakfast.same_group_items().order_by("pk")[0]
>>> first_gen_instance.latest_instance()
<MySampleModel: MySampleModel object (3)>
```

Throws a DoesNotExist exception if the object does not exist.


### earliest_instance

Returns the oldest object in the Stackgroup to which its own object belongs.

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> [instance_breakfast.save() for i in range(2)]
>>> third_gen_instance = instance_breakfast.same_group_items().order_by("pk")[2]
>>> third_gen_instance.earliest_instance()
<MySampleModel: MySampleModel object (1)>
```

Throws a DoesNotExist exception if the object does not exist.


# License

MIT License
