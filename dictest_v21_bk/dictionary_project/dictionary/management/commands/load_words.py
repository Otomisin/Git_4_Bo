import json
import math  # For checking NaN
from django.core.management.base import BaseCommand
from dictionary.models import Word
import os
from django.conf import settings


class Command(BaseCommand):
    help = "Load words from JSON file into the database"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(
            settings.BASE_DIR, 'dictionary', 'dictionary_file', 'sample_words.json')

        try:
            # Check if the file exists
            if not os.path.exists(file_path):
                self.stderr.write(f"File not found: {file_path}")
                return

            # Print the file path for debugging
            self.stdout.write(f"Attempting to read file: {file_path}")

            # Try to read raw file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.stdout.write(f"File length: {len(content)} characters")
                self.stdout.write(f"First 100 characters: {content[:100]}")

                # Return to beginning of file
                f.seek(0)

                # Try to parse JSON
                data = json.load(f)

                for item in data:
                    # Replace NaN with None
                    cleaned_item = {
                        key: (None if isinstance(value, float)
                              and math.isnan(value) else value)
                        for key, value in item.items()
                    }

                    # Insert or update the Word object
                    Word.objects.update_or_create(
                        word=cleaned_item.get("word"),
                        defaults={
                            "definition": cleaned_item.get("definition"),
                            "example": cleaned_item.get("example"),
                            "Yoruba_Word": cleaned_item.get("Yoruba_Word"),
                            "English_Word": cleaned_item.get("English_Word"),
                            "Examples_in_English": cleaned_item.get("Examples_in_English"),
                            "Examples_in_Yoruba": cleaned_item.get("Examples_in_Yoruba"),
                            "Audio_in_Yoruba": cleaned_item.get("Audio_in_Yoruba"),
                            "Audio_in_English": cleaned_item.get("Audio_in_English"),
                            "Grammar_Category": cleaned_item.get("Grammar_Category"),
                            "Plural_Form": cleaned_item.get("Plural_Form"),
                            "Root_Word": cleaned_item.get("Root_Word"),
                            "Synonyms": cleaned_item.get("Synonyms"),
                            "Antonyms": cleaned_item.get("Antonyms"),
                            "Proverbs_or_Idioms": cleaned_item.get("Proverbs_or_Idioms"),
                            "Common_Phrases": cleaned_item.get("Common_Phrases"),
                            "Tonal_Marks": cleaned_item.get("Tonal_Marks"),
                            "Dialect": cleaned_item.get("Dialect"),
                            "Cultural_Note": cleaned_item.get("Cultural_Note"),
                            "Etymology": cleaned_item.get("Etymology"),
                            "Usage_Category": cleaned_item.get("Usage_Category"),
                            "Word_Frequency": cleaned_item.get("Word_Frequency"),
                            "Difficulty_Level": cleaned_item.get("Difficulty_Level"),
                            "Images": cleaned_item.get("Images"),
                            "caption": cleaned_item.get("caption"),
                            "Related_Words": cleaned_item.get("Related_Words"),
                            "Interactive_Elements": cleaned_item.get("Interactive_Elements"),
                            "Notes": cleaned_item.get("Notes"),
                            "Tags": cleaned_item.get("Tags"),
                            "word_source": cleaned_item.get("word_source"),
                        },
                    )
                self.stdout.write(self.style.SUCCESS(
                    "Words loaded successfully"))
        except Exception as e:
            self.stderr.write(f"Error loading data: {e}")
