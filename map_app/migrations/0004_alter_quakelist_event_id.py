# Generated by Django 4.2.5 on 2023-10-13 06:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("map_app", "0003_quakelist_event_id_alter_quakedetail_event_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quakelist",
            name="event_id",
            field=models.IntegerField(),
        ),
    ]
