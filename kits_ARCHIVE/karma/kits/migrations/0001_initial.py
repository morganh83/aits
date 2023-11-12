# Generated by Django 4.1 on 2022-09-17 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='banLength',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banLen', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='dinoName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dino', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='punishTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('steamId', models.IntegerField(blank=True, default=0, null=True)),
                ('userName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('punishment', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('banTime', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('banTimeOther', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('reason', models.TextField(blank=True, default='', max_length=1000, null=True)),
                ('courtesy', models.BooleanField(blank=True, default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('modName', models.CharField(blank=True, default='', max_length=100)),
                ('addtlMods', models.CharField(blank=True, default='', max_length=100)),
                ('ticketLink', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('counterLink', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='revTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('modName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('addtlMods', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('userName', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('discName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('steamId', models.IntegerField(blank=True, default=0, null=True)),
                ('growth', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True)),
                ('dinoName', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('revd', models.BooleanField(blank=True, default=False)),
                ('ticketLink', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('counterLink', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rules', models.CharField(max_length=6, unique=True)),
                ('description', models.CharField(max_length=400, unique=True)),
                ('clarity', models.TextField(blank=True, default='', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='strikeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strike', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='brokenRules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rules', models.CharField(blank=True, max_length=6, null=True)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
                ('clarity', models.TextField(blank=True, default='', max_length=2000)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brokenRules', to='kits.punishticket')),
            ],
        ),
    ]