# Generated by Django 2.2.4 on 2019-10-18 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20191018_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='user',
        ),
    ]