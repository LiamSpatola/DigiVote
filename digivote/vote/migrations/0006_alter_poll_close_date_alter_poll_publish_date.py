# Generated by Django 5.1.1 on 2024-09-15 02:10

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vote", "0005_alter_poll_close_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="poll",
            name="close_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 9, 16, 2, 10, 32, 898513, tzinfo=datetime.timezone.utc
                ),
                verbose_name="close date",
            ),
        ),
        migrations.AlterField(
            model_name="poll",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 9, 15, 2, 10, 32, 898513, tzinfo=datetime.timezone.utc
                ),
                verbose_name="date published",
            ),
        ),
    ]
