# Generated by Django 3.2.13 on 2023-02-19 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_history_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='author',
        ),
    ]
