# Generated by Django 3.2.13 on 2023-02-19 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20230219_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='author',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main.customuser', verbose_name='Автор'),
            preserve_default=False,
        ),
    ]
