# Generated by Django 4.2.4 on 2023-08-10 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0002_rename_end_data_tasks_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='status',
            field=models.IntegerField(default='', max_length=2),
        ),
    ]