# Generated by Django 4.2.7 on 2024-03-08 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integer', '0003_datapool'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapool',
            name='testing',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
