# Generated by Django 4.2.7 on 2024-03-08 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('integer', '0002_delete_dataloggerdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='datapool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='integer.device_tag_setting')),
            ],
        ),
    ]
