# Generated by Django 2.1.4 on 2019-01-17 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0044_add_decimal_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributevaluechoice',
            name='value',
            field=models.TextField(verbose_name='value'),
        ),
    ]
