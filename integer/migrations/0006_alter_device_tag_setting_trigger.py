# Generated by Django 4.2.7 on 2024-03-09 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('integer', '0005_triggerconfiguration_remove_device_tag_setting_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_tag_setting',
            name='trigger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='integer.triggerconfiguration'),
        ),
    ]
