# Generated by Django 4.1.1 on 2022-09-26 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shortener", "0002_userdetail"),
    ]

    operations = [
        migrations.DeleteModel(name="UserDetail",),
    ]