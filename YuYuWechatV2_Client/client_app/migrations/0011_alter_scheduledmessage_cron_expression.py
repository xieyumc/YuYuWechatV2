# Generated by Django 4.1 on 2024-07-20 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0010_alter_scheduledmessage_cron_expression'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledmessage',
            name='cron_expression',
            field=models.CharField(max_length=255),
        ),
    ]