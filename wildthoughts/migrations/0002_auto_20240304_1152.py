# Generated by Django 2.2.28 on 2024-03-04 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildthoughts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='website',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
