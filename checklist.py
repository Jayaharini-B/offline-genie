import json

def get_checklist(location):
    with open("data/checklist.json", "r") as file:
        data = json.load(file)
    if location in data:
        items = data[location]
        return f"Checklist for {location}: " + ", ".join(items)
    return "I have no checklist for that location."
