import os
import json
from fuzzywuzzy import fuzz

# Load translator data
def load_translator_data():
    base_path = os.path.abspath(os.path.dirname(__file__))

    file_path = os.path.join(base_path, 'data', 'translation_phrases.json')  # ✅ Updated filename
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

translator_data = load_translator_data()

# Find the closest phrase using fuzzy matching
def find_closest_phrase(command):
    best_match = None
    best_score = 0
    for phrase in translator_data:
        score = fuzz.partial_ratio(phrase.lower(), command)
        if score > best_score:
            best_score = score
            best_match = phrase
    return best_match if best_score >= 70 else None

# Find the closest language
def find_closest_language(command, languages):
    best_lang = None
    best_score = 0
    for lang in languages:
        score = fuzz.partial_ratio(lang.lower(), command)
        if score > best_score:
            best_score = score
            best_lang = lang
    return best_lang if best_score >= 70 else None

# Final translation function
def translate_phrase(command):
    command = command.lower()
    print("🔍 Looking to translate:", command)

    phrase = find_closest_phrase(command)
    if phrase:
        lang = find_closest_language(command, translator_data[phrase])
        if lang:
            return f'"{phrase}" in {lang.capitalize()} is "{translator_data[phrase][lang]}".'
        else:
            return "I found the phrase but couldn’t find the language."
    return "Sorry, I can’t translate that yet."

# ✅ Quick test examples
if __name__ == "__main__":
    tests = [
        "how are you in hindi",
        "thank you in french",
        "good morning in tamil"
    ]
    for t in tests:
        print(translate_phrase(t))
