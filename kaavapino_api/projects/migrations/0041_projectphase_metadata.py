# Generated by Django 2.1.2 on 2018-12-12 12:41

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0040_add_project_fields_to_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectphase',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='metadata'),
        ),
    ]
