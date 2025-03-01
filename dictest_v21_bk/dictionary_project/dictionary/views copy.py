# dictionary/views.py
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Word
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Word

# def home(request):
#     query = request.GET.get('q', '').strip()
#     if query:
#         # Instead of showing results on home page, redirect to word detail
#         word = Word.objects.filter(word__iexact=query).first()
#         if word:
#             return redirect('word_detail', pk=word.pk)
#         # If no exact match, maybe redirect to a "not found" page or stay on home
#         return render(request, 'dictionary/home.html', {
#             'show_hero': True,
#             'no_results': True
#         })
    
#     return render(request, 'dictionary/home.html', {
#         'show_hero': True,
#         'is_homepage': True
#     })


def home(request):
    query = request.GET.get('q', '').strip()
    if query:
        # Filter by `word_source` and order alphabetically
        word = Word.objects.filter(word__iexact=query, word_source="Samples").order_by('word').first()
        if word:
            return redirect('word_detail', pk=word.pk)
        return render(request, 'dictionary/home.html', {
            'show_hero': True,
            'no_results': True
        })

    return render(request, 'dictionary/home.html', {
        'show_hero': True,
        'is_homepage': True
    })




# def search_suggestions(request):
#     query = request.GET.get('q')
#     if query:
#         suggestions = Word.objects.filter(word__icontains=query).values('word', 'definition')[:5]
#         formatted_suggestions = [
#             {
#                 "word": item['word'].title(),  # Convert word to Proper Case
#                 "html": f"<strong>{item['word'].title()}</strong>: <span style='font-style: italic; font-size: 0.85em;'>{item['definition']}</span>"  # Formatted display
#             }
#             for item in suggestions
#         ]

#         return JsonResponse(formatted_suggestions, safe=False)
#     return JsonResponse([])


# def word_detail(request, pk):
#     # Get single word by primary key
#     word = get_object_or_404(Word, pk=pk)
    
#     # Add debug print to verify we're getting the correct word
#     print(f"Displaying word: {word.word} (ID: {pk})")
    
#     return render(request, 'dictionary/word_detail.html', {
#         'word': word,
#         'show_hero': False  # Add this to control hero section display
#     })

def word_detail(request, pk):
    # Get single word by primary key
    word = get_object_or_404(Word, pk=pk)
    
    # Prepare additional context for the template
    context = {
        'word': word,
        'show_hero': False,  # Control hero section display
        'yoruba_word': word.Yoruba_Word,
        'english_word': word.English_Word,
        'examples_in_english': word.Examples_in_English,
        'examples_in_yoruba': word.Examples_in_Yoruba,
        'definition_yoruba': word.definition_yoruba,
        'audio_in_yoruba': word.Audio_in_Yoruba.url if word.Audio_in_Yoruba else None,
        'audio_in_english': word.Audio_in_English.url if word.Audio_in_English else None,
        'grammar_category': word.Grammar_Category,
        'cultural_note': word.Cultural_Note,
        'synonyms': word.Synonyms.split(',') if word.Synonyms else [],
        'antonyms': word.Antonyms.split(',') if word.Antonyms else [],
    }
    
    return render(request, 'dictionary/word_detail.html', context)



# def search_suggestions(request):
#     query = request.GET.get('q')
#     if query:
#         # Use `startswith` for matching words from the beginning
#         suggestions = Word.objects.filter(word__istartswith=query).values('word', 'definition')[:9]
#         formatted_suggestions = [
#             {
#                 "word": item['word'].title(),
#                 "html": f"<strong>{item['word'].title()}</strong>: <span style='font-style: italic; font-size: 0.85em;'>{item['definition']}</span>"
#             }
#             for item in suggestions
#         ]
#         return JsonResponse(formatted_suggestions, safe=False)
#     return JsonResponse([])


def search_suggestions(request):
    query = request.GET.get('q')
    if query:
        # Ensure words come from `Samples` source and are alphabetically ordered
        suggestions = Word.objects.filter(word__istartswith=query, word_source="Samples").order_by('word').values('word', 'definition')[:9]
        formatted_suggestions = [
            {
                "word": item['word'].title(),
                "html": f"<strong>{item['word'].title()}</strong>: <span style='font-style: italic; font-size: 0.85em;'>{item['definition']}</span>"
            }
            for item in suggestions
        ]
        return JsonResponse(formatted_suggestions, safe=False)
    return JsonResponse([])


# def random_word(request):
#     word = Word.objects.order_by('?').first()  # Fetch a random word
#     return render(request, 'dictionary/word_detail.html', {'word': word})

def random_word(request):
    # Fetch a random word with `word_source="Samples"`
    word = Word.objects.filter(word_source="Samples").order_by('?').first()
    return render(request, 'dictionary/word_detail.html', {'word': word})




