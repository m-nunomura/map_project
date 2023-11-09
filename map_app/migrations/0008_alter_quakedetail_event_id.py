# Generated by Django 4.2.5 on 2023-10-17 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("map_app", "0007_remove_quakelist_max_seismic_intensity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quakedetail",
            name="event_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="map_app.quakelist"
            ),
        ),
    ]
