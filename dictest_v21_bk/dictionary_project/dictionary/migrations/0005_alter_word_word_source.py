# Generated by Django 5.1.2 on 2024-11-24 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_word_definition_yoruba_word_word_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='word_source',
            field=models.CharField(blank=True, default='sample', max_length=200, null=True),
        ),
    ]
