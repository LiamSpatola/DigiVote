# Generated by Django 5.1.1 on 2024-09-15 02:15

import django.utils.timezone
import vote.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vote", "0007_alter_poll_close_date_alter_poll_publish_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="poll",
            name="close_date",
            field=models.DateTimeField(
                default=vote.models.get_default_close_date, verbose_name="close date"
            ),
        ),
        migrations.AlterField(
            model_name="poll",
            name="publish_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="date published"
            ),
        ),
    ]