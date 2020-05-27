# Generated by Django 3.0.6 on 2020-05-25 11:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stack_group_uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('test_field', models.CharField(max_length=100)),
            ],
            options={
                'get_latest_by': 'pk',
                'abstract': False,
            },
        ),
    ]