from googletrans import Translator

def translate_text_to_english(text):
    """
    Translates the given text to English.
    
    Args:
    text (str): The text to translate.
    
    Returns:
    str: The translated text in English.
    """
    translator = Translator()
    try:
        translated_text = translator.translate(text, dest='en').text
        return translated_text
    except Exception as e:
        return f"Error translating text: {e}"
