# Generated by Django 2.1.4 on 2019-01-22 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0046_projectphasesectionattribute_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='unit',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='unit'),
        ),
    ]
