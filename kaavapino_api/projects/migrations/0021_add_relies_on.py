# Generated by Django 2.1.2 on 2018-10-25 08:00

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_update_meta_and_attributedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectphasesectionattribute',
            name='relies_on',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_section_attribute', to='projects.ProjectPhaseSectionAttribute', verbose_name='relies on'),
        ),
    ]
