# Generated by Django 3.0.8 on 2022-09-09 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader_app', '0004_auto_20220909_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]