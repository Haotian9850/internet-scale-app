# Generated by Django 2.2.4 on 2019-10-19 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_pet_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenticator',
            name='authenticator',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]