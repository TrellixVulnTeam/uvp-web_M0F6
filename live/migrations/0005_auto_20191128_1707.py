# Generated by Django 2.2.7 on 2019-11-28 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("live", "0004_feature_current_guests"),
    ]

    operations = [
        migrations.DeleteModel(name="MediaPlayer",),
        migrations.AddField(
            model_name="feature",
            name="channel_name",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
