# Generated by Django 2.1.2 on 2018-12-12 13:15

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_projectphase_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='deadlines',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='deadlines'),
        ),
    ]
