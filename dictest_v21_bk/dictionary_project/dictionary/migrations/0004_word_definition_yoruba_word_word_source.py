# Generated by Django 5.1.2 on 2024-11-24 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_word_antonyms_word_audio_in_english_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='definition_yoruba',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='word',
            name='word_source',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
