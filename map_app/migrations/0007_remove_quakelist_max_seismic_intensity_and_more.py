# Generated by Django 4.2.5 on 2023-10-16 08:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("map_app", "0006_citylist"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quakelist",
            name="max_seismic_intensity",
        ),
        migrations.AlterField(
            model_name="quakedetail",
            name="event_id",
            field=models.CharField(max_length=100),
        ),
    ]