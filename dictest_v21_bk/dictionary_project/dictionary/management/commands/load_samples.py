import json
import os
from django.core.management.base import BaseCommand
from dictionary.models import Word
from django.conf import settings


class Command(BaseCommand):
    help = "Load sample words from JSON file into the database"

    def handle(self, *args, **kwargs):
        # Use a relative path that will work on any system
        sample_file_path = os.path.join(settings.BASE_DIR, 'C:\Users\orena\OneDrive\01_ORENAIKE\02_CAREER_AND_DEVELOPMENTS\SkillsIT\Python\django\dictest_v21\dictionary_project\dictionary\dictionary_file\sample_words.json')

        # Check if file exists
        if not os.path.exists(sample_file_path):
            self.stderr.write(self.style.ERROR(
                f"File not found: {sample_file_path}"))
            self.stderr.write(self.style.WARNING(
                "Please create this file using the sample JSON provided"))
            return

        try:
            with open(sample_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                words_added = 0

                for item in data:
                    # Handle potential missing fields
                    word_obj, created = Word.objects.update_or_create(
                        word=item.get("word"),
                        defaults={
                            "definition": item.get("definition", ""),
                            "example": item.get("example", ""),
                            "Yoruba_Word": item.get("Yoruba_Word"),
                            "English_Word": item.get("English_Word"),
                            "Examples_in_English": item.get("Examples_in_English"),
                            "Examples_in_Yoruba": item.get("Examples_in_Yoruba"),
                            "Grammar_Category": item.get("Grammar_Category"),
                            "Synonyms": item.get("Synonyms"),
                            "Antonyms": item.get("Antonyms"),
                            "Cultural_Note": item.get("Cultural_Note"),
                            "word_source": "Samples"  # Ensure this is set to match your views
                        },
                    )

                    if created:
                        words_added += 1
                        self.stdout.write(f"Added: {item.get('word')}")
                    else:
                        self.stdout.write(f"Updated: {item.get('word')}")

                self.stdout.write(self.style.SUCCESS(
                    f"Loaded {words_added} new words successfully"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f"Error loading data: {str(e)}"))
