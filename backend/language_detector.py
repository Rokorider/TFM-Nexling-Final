from fast_langdetect import detect

SUPPORTED_LANGUAGES = {
    "es", "en", "fr", "de", "it",
    "pt", "nl", "ru", "zh", "ja",
}


def detect_language(text: str) -> str | None:
    """Detecta el idioma y comprueba que esté admitido."""

    text = text.strip()

    if not text:
        return None
    
    # No intentar detectar el idioma si no hay letras.
    if not any(character.isalpha() for character in text):
        return None

    try:
        results = detect(text, model="lite")

        if not results:
            return None

        detected_language = results[0].get("lang")

        if detected_language in SUPPORTED_LANGUAGES:
            return detected_language

        return None

    except Exception:
        return None
