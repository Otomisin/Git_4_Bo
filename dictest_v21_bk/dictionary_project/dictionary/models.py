from django.db import models  # Ensure this import is at the top

class Word(models.Model):
    # Existing fields
    word = models.CharField(max_length=200, unique=True)
    definition = models.TextField()
    example = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Only auto_now_add, no default

    # New fields
    Yoruba_Word = models.CharField(max_length=200, null=True, blank=True)
    English_Word = models.CharField(max_length=200, null=True, blank=True)
    Examples_in_English = models.TextField(null=True, blank=True)
    Examples_in_Yoruba = models.TextField(null=True, blank=True)
    definition_yoruba = models.TextField(null=True, blank=True)
    Audio_in_Yoruba = models.FileField(upload_to="audio/yoruba/", null=True, blank=True)
    Yoruba_Word = models.CharField(max_length=200, null=True, blank=True)
    Audio_in_English = models.FileField(upload_to="audio/english/", null=True, blank=True)
    Grammar_Category = models.CharField(max_length=100, null=True, blank=True)
    Plural_Form = models.CharField(max_length=200, null=True, blank=True)
    Root_Word = models.CharField(max_length=200, null=True, blank=True)
    Synonyms = models.TextField(null=True, blank=True)
    Antonyms = models.TextField(null=True, blank=True)
    Proverbs_or_Idioms = models.TextField(null=True, blank=True)
    Common_Phrases = models.TextField(null=True, blank=True)
    Tonal_Marks = models.CharField(max_length=50, null=True, blank=True)
    Dialect = models.CharField(max_length=100, null=True, blank=True)
    Cultural_Note = models.TextField(null=True, blank=True)
    Etymology = models.TextField(null=True, blank=True)
    Usage_Category = models.CharField(max_length=100, null=True, blank=True)
    Word_Frequency = models.IntegerField(null=True, blank=True)
    Difficulty_Level = models.CharField(max_length=100, null=True, blank=True)
    Images = models.ImageField(upload_to="images/", null=True, blank=True)
    caption = models.CharField(max_length=200, blank=True, null=True)
    Related_Words = models.TextField(null=True, blank=True)
    Interactive_Elements = models.TextField(null=True, blank=True)
    Notes = models.TextField(null=True, blank=True)
    Tags = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    word_source = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        # Updated to include both old and new field names
        return f"{self.word} / {self.Yoruba_Word}"