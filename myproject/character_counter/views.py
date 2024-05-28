from django.shortcuts import render
from .utils import count_characters_in_csv, count_characters_in_text, count_characters_and_words

def character_counter(request):
    characters_in_csv = None
    words_in_csv = None
    characters_in_txt = None
    words_in_txt = None
    characters_in_input = None
    words_in_input = None

    if request.method == 'POST':
        if request.FILES.get('file'):
            uploaded_file = request.FILES['file']
            if uploaded_file.name.endswith('.csv'):
                characters_in_csv, words_in_csv = count_characters_in_csv(uploaded_file)
            elif uploaded_file.name.endswith('.txt'):
                characters_in_txt, words_in_txt = count_characters_in_text(uploaded_file)
        if 'input_text' in request.POST:
            input_text = request.POST['input_text']
            characters_in_input, words_in_input = count_characters_and_words(input_text)

    return render(request, 'character_counter.html', {
        'characters_in_csv': characters_in_csv,
        'words_in_csv': words_in_csv,
        'characters_in_txt': characters_in_txt,
        'words_in_txt': words_in_txt,
        'characters_in_input': characters_in_input,
        'words_in_input': words_in_input
    })
