from django.core.management.base import BaseCommand
from ....dictionary_utils import load_dictionary
from ....models import Word


class Command(BaseCommand):
    help = 'Loads the dictionary data from the JSON file'

    def handle(self, *args, **options):
        # Path to your JSON file
        path = r"C:\Users\orenaike\OneDrive\01_ORENAIKE\02_CAREER_AND_DEVELOPMENTS\SkillsIT\Python\django\dictest_v2\dictionary_project\dictionary\dictionary_file\dictionary_compact.json"
        # Ensure this function transforms the JSON appropriately
        dictionary_data = load_dictionary(path)

        if not dictionary_data:
            self.stdout.write(self.style.ERROR(
                'Failed to load dictionary data'))
            return

        for entry in dictionary_data:
            try:
                word_obj, created = Word.objects.get_or_create(
                    word=entry['word'],
                    defaults={
                        'definition': entry['definition'],
                        # Default example text
                        'example': entry.get('example', "No example available."),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Added new word: {word_obj.word}"))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Word already exists: {word_obj.word}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error saving word: {entry.get('word', 'Unknown')} - {e}"))

        self.stdout.write(self.style.SUCCESS(
            'Dictionary data loading complete'))
