# Generated by Django 3.2.7 on 2023-12-31 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, default='', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='languages',
            field=models.CharField(blank=True, default='English', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='timezeone',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]