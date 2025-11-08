from translator import translate_phrase
from navigation import get_navigation_path

def respond(command):
    command = command.lower().strip()

    # 🔁 Handle navigation command
    if "navigate from" in command and "to" in command:
        try:
            parts = command.split("navigate from")[1].split("to")
            source = parts[0].strip()
            destination = parts[1].strip()
            return get_navigation_path(source, destination)
        except Exception as e:
            return f"Couldn't parse navigation command. Please say: 'navigate from [source] to [destination]'. Error: {e}"

    # 🌍 Handle translation commands
    if "translate" in command or "how to say" in command or "in" in command:
        return translate_phrase(command)

    # 🙏 Gratitude
    if "thank you" in command:
        return "You're welcome!"

    # 🧠 Identity
    if "your name" in command:
        return "I am Offline Genie, your travel buddy."

    # Default fallback
    return "Sorry, I didn’t understand that."
