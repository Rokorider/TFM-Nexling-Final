from translator import translate_text
from language_detector import detect_language


def test_language_detection():
    print("\n=== PRUEBAS DE DETECCIÓN DE IDIOMA ===")

    cases = [
        ("Hola, ¿cómo estás? Me gustaría aprender idiomas.", "es"),
        ("Hello, how are you? I want to learn new languages.", "en"),
        ("", None),
        ("12345", None),
    ]

    for text, expected in cases:
        result = detect_language(text)

        if result == expected:
            status = "OK"
        else:
            status = "REVISAR"

        print(f"Texto: {text!r}")
        print(f"Esperado: {expected} | Obtenido: {result} | {status}")
        print("-" * 50)


def test_translation_robustness():
    print("\n=== PRUEBAS DE ROBUSTEZ DE TRADUCCIÓN ===")

    # Comprobar que un texto vacío no se traduce.
    try:
        translate_text("", "es", "en")
        print("Texto vacío: REVISAR (no se ha producido un error)")
    except ValueError as e:
        print(f"Texto vacío: OK (se ha rechazado la entrada) - {e}")
    except Exception as e:
        print(f"Texto vacío: REVISAR (error inesperado) - {e}")

    # Comprobar que un idioma no admitido se rechaza.
    try:
        translate_text("Hola, ¿qué tal?", "xx", "en")
        print("Idioma no admitido: REVISAR (no se ha producido un error)")
    except Exception:
        print("Idioma no admitido: OK (se ha rechazado la entrada)")

    # Comprobar la conservación de los saltos de línea.
    text = "Buenos días.\n¿Cómo estás?\nHasta mañana."

    try:
        result = translate_text(text, "es", "en")

        print("\nPrueba de saltos de línea:")
        print(f"Original: {text!r}")
        print(f"Traducción: {result!r}")

        if "\n" in result:
            print("Saltos de línea: OK")
        else:
            print("Saltos de línea: REVISAR")

    except Exception as error:
        print(f"Error en la prueba de saltos de línea: {error}")
        print("\n=== PRUEBAS DE FRASES CORTAS ===")

    short_sentences = [
        "Buenos días.",
        "¿Cómo estás?",
        "Hasta mañana.",
        "Me llamo Javier.",
    ]

    for sentence in short_sentences:
        try:
            result = translate_text(sentence, "es", "en")
            print(f"Original: {sentence}")
            print(f"Traducción: {result}")
        except Exception as error:
            print(f"Error al traducir {sentence!r}: {error}")

        print("-" * 50)

    print("\n=== PRUEBAS ADICIONALES DE TRADUCCIÓN ===")

    additional_cases = [
        ("Gracias por tu ayuda.", "es", "en"),
        ("¿Dónde está la estación?", "es", "en"),
        ("I am happy to see you.", "en", "es"),
    ]

    for text, source_lang, target_lang in additional_cases:
        try:
            result = translate_text(text, source_lang, target_lang)
            print(f"Original: {text}")
            print(f"Traducción: {result}")
        except Exception as error:
            print(f"Error al traducir {text!r}: {error}")

        print("-" * 50)


if __name__ == "__main__":
    test_language_detection()
    test_translation_robustness()