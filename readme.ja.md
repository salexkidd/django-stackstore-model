Django Staskstore model
=========================================================================================

Djanog Stackstoreは最小の手順でモデルのバージョニングをサポートすることができるライブラリです。

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

各Stackgroupの最新のオブジェクトのクエリセットを返します。

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

各Stackgroupの最新のオブジェクト群から照合パラメタに一致するオブジェクトを返します。

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

オブジェクトがsaveされると新しいオブジェクトが生成され、save元のオブジェクトと同一のstack_group_uuidが割り当てられます。
つまり新しいバージョンが生成されることになります。

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> instance_breakfast.body = "Fried Egg with bread"
>>> instance_breakfast.save() # Save method create version object <MySampleModel: MySampleModel object (2)>
>>> MySampleModel.objects.all()
<StackStoreQuerySet [<MySampleModel: MySampleModel object (1)>, <MySampleModel: MySampleModel object (2)>]>
```

新しいバージョンを作成せずに上書き保存をしたい場合は `save` メソッドに `__create_new_version` に `False` を渡します。

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg")
>>> instance_breakfast.save(__create_new_version=False)
>>> instance_breakfast.pk
1
```

### force_delete

オブジェクトを削除します。

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> MySampleModel.objects.all()
<StackStoreQuerySet [<MySampleModel: MySampleModel object (1)>]>
>>> instance_breakfast.force_delete()
>>> MySampleModel.objects.all()
<StackStoreQuerySet []>
```

既存の`delete`メソッドを呼び出すとNotImplementedError例外を送出します。

### same_group_items

同一のStackgroupに属しているすべてのオブジェクトを返すQuerySetを返します。

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> [instance_breakfast.save() for i in range(2)]
>>> instance_breakfast.same_group_items()
<StackStoreQuerySet [<MySampleModel: MySampleModel object (3)>, <MySampleModel: MySampleModel object (2)>, <MySampleModel: MySampleModel object (1)>]>
```


### previous_instance

一つ前のバージョンのオブジェクトを返します。

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> [instance_breakfast.save() for i in range(2)]
>>> second_gen_instance = instance_breakfast.same_group_items().order_by("pk")[1]
>>> second_gen_instance.previous_instance()
<MySampleModel: MySampleModel object (1)>
```

該当するオブジェクトが存在しない場合、DoesNotExist例外を送出します。


### next_instance

次のバージョンのオブジェクトを返します。

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> [instance_breakfast.save() for i in range(2)]
>>> second_gen_instance = instance_breakfast.same_group_items()[1]
>>> second_gen_instance.next_instance()
<MySampleModel: MySampleModel object (3)>
```

該当するオブジェクトが存在しない場合、DoesNotExist例外を送出します。


### latest_instance

自身のオブジェクトが属するStackgroupの最新のオブジェクトを返します。

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> [instance_breakfast.save() for i in range(2)]
>>> first_gen_instance = instance_breakfast.same_group_items().order_by("pk")[0]
>>> first_gen_instance.latest_instance()
<MySampleModel: MySampleModel object (3)>
```

該当するオブジェクトが存在しない場合、DoesNotExist例外を送出します。


### earliest_instance

自身のオブジェクトが属するStackgroupの最古のオブジェクトを返します。

```
>>> instance_breakfast = MySampleModel.objects.create(title="Today's breakfast", body="Spam with Egg") # Create <MySampleModel: MySampleModel object (1)>
>>> [instance_breakfast.save() for i in range(2)]
>>> third_gen_instance = instance_breakfast.same_group_items().order_by("pk")[2]
>>> third_gen_instance.earliest_instance()
<MySampleModel: MySampleModel object (1)>
```

該当するオブジェクトが存在しない場合、DoesNotExist例外を送出します。
