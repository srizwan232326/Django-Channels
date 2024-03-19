# Generated by Django 4.2.7 on 2024-03-17 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('integer', '0010_remove_triggerconfiguration_trigger_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='Triggerlogger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.IntegerField()),
                ('trigger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integer.triggerconfiguration')),
            ],
        ),
    ]