import sounddevice as sd
import numpy as np
import noisereduce as nr
import vosk
import queue
import json
import sys
import pyttsx3
from fuzzywuzzy import fuzz
from datetime import datetime, timedelta

# Initialize Vosk model
model = vosk.Model("vosk-model-small-en-us-0.15")
rec = vosk.KaldiRecognizer(model, 16000)

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)

# Load data files
with open('data/currency_rates.json', 'r', encoding='utf-8') as f:
    currency_data = json.load(f)

with open('data/translation_phrases.json', 'r', encoding='utf-8') as f:
    translation_data = json.load(f)

with open('data/packing_checklists.json', 'r', encoding='utf-8') as f:
    checklist_data = json.load(f)

with open('data/timezones.json', 'r', encoding='utf-8') as f:
    timezone_data = json.load(f)

with open('data/weather_conditions.json', 'r', encoding='utf-8') as f:
    weather_data = json.load(f)

with open('data/emergency_contacts.json', 'r', encoding='utf-8') as f:
    emergency_data = json.load(f)

with open('data/safety_tips.json', 'r', encoding='utf-8') as f:
    safety_data = json.load(f)

# Listen function
def listen():
    print("🎤 Speak now...")

    # Record a short noise sample for profiling (1 second)
    print("Recording background noise...")
    noise_sample = sd.rec(int(16000 * 1), samplerate=16000, channels=1, dtype='int16')
    sd.wait()

    # Record actual speech input (5 seconds)
    print("Recording your command...")
    audio = sd.rec(int(16000 * 5), samplerate=16000, channels=1, dtype='int16')
    sd.wait()

    # Convert both to float32 for noisereduce
    noise_sample = noise_sample.astype('float32')
    audio = audio.astype('float32')

    # Apply noise reduction
    reduced_noise = nr.reduce_noise(y=audio.flatten(), y_noise=noise_sample.flatten(), sr=16000)

    # Convert back to int16 for Vosk
    reduced_noise_int16 = reduced_noise.astype('int16')

    # Process with Vosk
    if rec.AcceptWaveform(reduced_noise_int16.tobytes()):
        result = json.loads(rec.Result())
        print("You said:", result['text'])
        return result['text']
    else:
        print("Sorry, I didn't catch that.")
        return ""

# Speak function
def speak(text):
    print("Genie says:", text)
    engine.say(text)
    engine.runAndWait()

# Translation function
def translate(command):
    phrase_match = None
    lang_match = None
    best_phrase_score = 0
    best_lang_score = 0

    for phrase in translation_data:
        score = fuzz.partial_ratio(phrase.lower(), command.lower())
        if score > best_phrase_score:
            best_phrase_score = score
            phrase_match = phrase

    if phrase_match:
        for lang in translation_data[phrase_match]:
            score = fuzz.partial_ratio(lang.lower(), command.lower())
            if score > best_lang_score:
                best_lang_score = score
                lang_match = lang

        if lang_match:
            return f'"{phrase_match}" in {lang_match.capitalize()} is "{translation_data[phrase_match][lang_match]}".'
        else:
            return "I found the phrase but couldn’t find the language."

    return "Sorry, I can’t translate that yet."

# Currency function
def currency(command):
    for country in currency_data:
        if country.lower() in command.lower():
            return f"{country} uses {currency_data[country]}."
    return "Sorry, I don't have currency information for that country."

# Checklist function
def checklist(command):
    best_loc = None
    best_score = 0
    for loc in checklist_data:
        score = fuzz.partial_ratio(loc.lower(), command.lower())
        if score > best_score:
            best_score = score
            best_loc = loc

    if best_loc and best_score >= 70:
        items = checklist_data[best_loc]
        return f"For {best_loc}, pack: {', '.join(items)}."
    else:
        return "Please mention a location like hill station or beach."

# Timezone function
def timezone_conversion(command):
    found_countries = []
    for country in timezone_data:
        if country.lower() in command.lower():
            found_countries.append(country)

    if len(found_countries) < 2:
        return "Please mention both source and target countries clearly."

    source = found_countries[0]
    target = found_countries[1]

    time_diff = timezone_data[target] - timezone_data[source]
    now = datetime.utcnow() + timedelta(hours=timezone_data[source])
    target_time = now + timedelta(hours=time_diff)

    source_time_str = now.strftime("%H:%M")
    target_time_str = target_time.strftime("%H:%M")

    return f"If it's {source_time_str} in {source}, then it's {target_time_str} in {target}."

# Weather function
def weather(command):
    for city in weather_data:
        if city.lower() in command.lower():
            return f"The weather in {city} is generally {weather_data[city]}."
    return "Sorry, I don't have climate info for that city."

# Emergency contacts function
def emergency(command):
    for country in emergency_data:
        if country.lower() in command.lower():
            contacts = emergency_data[country]
            contact_info = ', '.join([f"{k}: {v}" for k, v in contacts.items()])
            return f"Emergency contacts for {country}: {contact_info}."
    return "Sorry, I don't have emergency contact info for that country."

# Safety tips function
def safety(command):
    tips = []
    for country in safety_data:
        if country.lower() in command.lower():
            tips.extend(safety_data[country])

    if not tips and "general" in safety_data:
        tips = safety_data["General"]

    if tips:
        return "Here are some safety tips: " + ' '.join(tips)
    else:
        return "Sorry, I don't have safety tips for that country."

# Main loop
speak("Hello. I am Offline Genie, your travel buddy. How can I help you today?")

while True:
    command = listen()

    if command == "":
        continue
    elif "currency" in command:
        response = currency(command)
    elif "translate" in command or "say" in command:
        response = translate(command)
    elif "checklist" in command or "packing" in command:
        response = checklist(command)
    elif "time" in command and "in" in command:
        response = timezone_conversion(command)
    elif "weather" in command or "climate" in command:
        response = weather(command)
    elif "emergency" in command:
        response = emergency(command)
    elif "safety" in command or "tips" in command:
        response = safety(command)
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        sys.exit()
    else:
        response = "Sorry, I didn't understand that."

    speak(response)

