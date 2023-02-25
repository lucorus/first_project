# Generated by Django 3.2.13 on 2023-02-26 17:10

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20230225_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='first_image',
            field=models.ImageField(blank=True, upload_to='Album'),
        ),
        migrations.AlterField(
            model_name='album',
            name='fourth_image',
            field=models.ImageField(blank=True, upload_to='Album'),
        ),
        migrations.AlterField(
            model_name='album',
            name='second_image',
            field=models.ImageField(blank=True, upload_to='Album'),
        ),
        migrations.AlterField(
            model_name='album',
            name='third_image',
            field=models.ImageField(blank=True, upload_to='Album'),
        ),
        migrations.AlterField(
            model_name='history',
            name='album',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name=main.models.Album),
        ),
    ]
