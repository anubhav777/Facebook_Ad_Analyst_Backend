# Generated by Django 3.0.6 on 2020-05-14 08:38

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pagesdetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.CharField(max_length=128)),
                ('page_name', models.CharField(max_length=128)),
                ('socialmedia', django.contrib.postgres.fields.jsonb.JSONField()),
                ('page_info', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]