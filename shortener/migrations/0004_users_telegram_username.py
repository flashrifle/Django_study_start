# Generated by Django 4.1.1 on 2022-10-06 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortener", "0003_statistic_custom_params_trackingparams"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="telegram_username",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
