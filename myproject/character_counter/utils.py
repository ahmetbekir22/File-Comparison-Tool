import csv

def count_characters_in_csv(file):
    content = file.read().decode('utf-8').strip()
    total_characters = len(content)
    total_words = len(content.split())
    return total_characters, total_words

def count_characters_in_text(file):
    content = file.read().decode('utf-8').strip()
    total_characters = len(content)
    total_words = len(content.split())
    return total_characters, total_words

def count_characters_and_words(text):
    text = text.strip()
    total_characters = len(text)
    total_words = len(text.split())
    return total_characters, total_words
