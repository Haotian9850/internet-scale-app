# Generated by Django 2.2.4 on 2019-10-17 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('authenticator', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('date_created', models.DateTimeField()),
            ],
        ),
    ]