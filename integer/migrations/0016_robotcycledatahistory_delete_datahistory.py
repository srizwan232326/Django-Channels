# Generated by Django 4.2.7 on 2024-03-19 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integer', '0015_alter_device_tag_setting_data_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='RobotCycleDataHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daytime', models.DateTimeField(auto_now_add=True)),
                ('model', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('spare1', models.CharField(blank=True, max_length=100, null=True)),
                ('spare2', models.CharField(blank=True, max_length=100, null=True)),
                ('L_resin_Paint_cons', models.IntegerField(blank=True, null=True)),
                ('L_hardener_Paint_cons', models.IntegerField(blank=True, null=True)),
                ('L_ratio', models.IntegerField(blank=True, null=True)),
                ('R_resin_Paint_cons', models.IntegerField(blank=True, null=True)),
                ('R_hardener_Paint_cons', models.IntegerField(blank=True, null=True)),
                ('R_ratio', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='datahistory',
        ),
    ]
