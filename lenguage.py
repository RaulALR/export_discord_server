import json
import os


directory = os.path.dirname(os.path.realpath(__file__))


def load_translations(language_code):
    translations_path = os.path.join(directory, 'translations', f'{language_code}.json')
    with open(f'{translations_path}', 'r', encoding='utf-8') as file:
        return json.load(file)

translations = {
    "en": load_translations("en"),
    "es": load_translations("es")
}

def get_translation(ctx, message_key, settings):
    if ctx is None:
        return translations['es'].get(message_key, message_key)
    else:        
        if "lenguage" in settings and str(ctx.guild.id) in settings["lenguage"]:
            language_code = settings["lenguage"][str(ctx.guild.id)]
            return translations[language_code].get(message_key, message_key)
        else:
            return translations['es'].get(message_key, message_key)

def set_language(ctx, language_code: str, settings):
    settings["lenguage"][str(ctx.guild.id)] = language_code
    save_settings(settings)
    
def save_settings(settings):
    setting_path = os.path.join(directory, 'translations', f'settings.json')
    with open(setting_path, 'w') as file:
        json.dump(settings, file, indent=4)
        
def load_settings():
    settings_path = os.path.join(directory, 'translations', f'settings.json')
    try:
        with open(settings_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}