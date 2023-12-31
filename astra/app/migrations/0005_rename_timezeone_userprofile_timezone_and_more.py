# Generated by Django 4.1 on 2024-01-01 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_userprofile_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='timezeone',
            new_name='timezone',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='alts',
            field=models.TextField(blank=True, default='', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='discord_username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
