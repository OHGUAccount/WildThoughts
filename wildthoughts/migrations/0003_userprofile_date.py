# Generated by Django 2.2.28 on 2024-03-11 11:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wildthoughts', '0002_petition_decision_maker'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
