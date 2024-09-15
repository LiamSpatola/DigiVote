# Generated by Django 5.1.1 on 2024-09-15 06:44

import uuid

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vote", "0010_alter_vote_receipt_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="poll",
            name="open_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="open date"
            ),
        ),
        migrations.AlterField(
            model_name="vote",
            name="receipt_id",
            field=models.UUIDField(
                default=uuid.UUID("cba22df0-292f-4b69-ab25-587242cb1e2c"),
                editable=False,
                unique=True,
            ),
        ),
    ]
