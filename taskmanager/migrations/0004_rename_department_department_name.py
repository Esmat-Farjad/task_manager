# Generated by Django 4.2.4 on 2023-09-10 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0003_tasks_dept'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='department',
            new_name='name',
        ),
    ]