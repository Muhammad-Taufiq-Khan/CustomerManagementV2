# Generated by Django 3.1 on 2020-08-30 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200830_1329'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChildModel',
        ),
        migrations.DeleteModel(
            name='ParentModel',
        ),
    ]
