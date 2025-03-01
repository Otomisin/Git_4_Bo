from django.core.management.base import BaseCommand
from dictionary.models import Word

class Command(BaseCommand):
    help = 'Adds initial dictionary data'

    def handle(self, *args, **kwargs):
        words_data = [
            {
                'word': 'Serendipity',
                'definition': 'The occurrence and development of events by chance in a happy or beneficial way.',
                'example': 'The discovery of penicillin was a perfect example of serendipity.'
            },
            {
                'word': 'Ephemeral',
                'definition': 'Lasting for a very short time.',
                'example': 'The ephemeral beauty of sunset only lasted a few minutes.'
            },
            {
                'word': 'Ubiquitous',
                'definition': 'Present, appearing, or found everywhere.',
                'example': 'Mobile phones have become ubiquitous in modern society.'
            }
        ]

        for data in words_data:
            Word.objects.get_or_create(
                word=data['word'],
                defaults={
                    'definition': data['definition'],
                    'example': data['example']
                }
            )
