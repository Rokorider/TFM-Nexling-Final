from functools import lru_cache

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


MODEL_NAME = "facebook/nllb-200-distilled-600M"
@lru_cache(maxsize=1)
def load_tokenizer():
    return AutoTokenizer.from_pretrained(MODEL_NAME)

LANGUAGES = {
    "es": {"name": "Español", "model_code": "spa_Latn"},
    "en": {"name": "Inglés", "model_code": "eng_Latn"},
    "fr": {"name": "Francés", "model_code": "fra_Latn"},
    "de": {"name": "Alemán", "model_code": "deu_Latn"},
    "it": {"name": "Italiano", "model_code": "ita_Latn"},
    "pt": {"name": "Portugués", "model_code": "por_Latn"},
    "nl": {"name": "Neerlandés", "model_code": "nld_Latn"},
    "ru": {"name": "Ruso", "model_code": "rus_Cyrl"},
    "zh": {"name": "Chino simplificado", "model_code": "zho_Hans"},
    "ja": {"name": "Japonés", "model_code": "jpn_Jpan"},
}


@lru_cache(maxsize=1)
def load_translation_model():
    """Carga el modelo una sola vez y reutiliza sus recursos."""
    tokenizer = load_tokenizer()
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    model.generation_config.max_length = None
    model.generation_config.max_new_tokens = None
    model.eval()

    return tokenizer, model


def split_text_into_chunks(text, tokenizer, max_tokens=200):
    """Divide un texto en fragmentos que caben en el modelo."""

    if not text.strip():
        return []

    token_ids = tokenizer(
        text,
        add_special_tokens=False,
    )["input_ids"]

    if len(token_ids) <= max_tokens:
        return [text]

    import re

    # Intentamos dividir primero por oraciones.
    sentences = re.split(r"(?<=[.!?。！？])\s+", text)

    chunks = []
    current_chunk = ""

    def token_count(value):
        return len(
            tokenizer(
                value,
                add_special_tokens=False,
            )["input_ids"]
        )

    for sentence in sentences:
        candidate = (
            f"{current_chunk} {sentence}".strip()
            if current_chunk
            else sentence
        )

        if token_count(candidate) <= max_tokens:
            current_chunk = candidate
            continue

        if current_chunk:
            chunks.append(current_chunk)
            current_chunk = ""

        if token_count(sentence) <= max_tokens:
            current_chunk = sentence
            continue

        # Si una oración supera el límite,
        # dividimos por palabras.
        words = sentence.split()
        partial = ""

        for word in words:
            candidate = f"{partial} {word}".strip()

            if token_count(candidate) > max_tokens:
                if partial:
                    chunks.append(partial)
                    partial = ""

                if token_count(word) > max_tokens:
                    # Último recurso: fragmentar por caracteres.
                    piece = ""
                    for character in word:
                        if token_count(piece + character) > max_tokens:
                            if piece:
                                chunks.append(piece)
                            piece = character
                    partial = piece
                else:
                    partial = word
            else:
                partial = candidate

        if partial:
            current_chunk = partial

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def translate_single_text(
    text: str,
    source_lang: str,
    target_lang: str,
    tokenizer,
    model,
) -> str:
    """Traduce un fragmento de texto sin gestionar los saltos de línea."""

    tokenizer.src_lang = LANGUAGES[source_lang]["model_code"]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=False,
        max_length=512,
    )

    target_code = LANGUAGES[target_lang]["model_code"]
    target_token_id = tokenizer.convert_tokens_to_ids(target_code)

    if target_token_id == tokenizer.unk_token_id:
        raise RuntimeError(
            f"No se ha encontrado el código del idioma {target_lang}."
        )

    with torch.inference_mode():
        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=target_token_id,
            max_new_tokens=384,
            num_beams=1,
            repetition_penalty=1.1,
            no_repeat_ngram_size=3,
        )

    return tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True,
    )[0]


def translate_text(
    text: str,
    source_lang: str,
    target_lang: str,
) -> str:
    """Traduce el texto conservando sus saltos de línea."""

    text = text.strip()

    if not text:
        raise ValueError("El texto no puede estar vacío.")

    if source_lang not in LANGUAGES:
        raise ValueError(
            f"Idioma de origen no admitido: {source_lang}"
        )

    if target_lang not in LANGUAGES:
        raise ValueError(
            f"Idioma de destino no admitido: {target_lang}"
        )

    if source_lang == target_lang:
        return text

    tokenizer, model = load_translation_model()

    print("max_length configurado:", model.generation_config.max_length)
    print("max_new_tokens configurado:", model.generation_config.max_new_tokens)

    # Conserva las líneas y los espacios en blanco entre ellas.
    lines = text.split("\n")
    translated_lines = []

    for line in lines:
        # No enviamos líneas vacías al modelo.
        if not line.strip():
            translated_lines.append(line)
            continue

        # Conservamos los espacios al principio y al final.
        leading_spaces = line[:len(line) - len(line.lstrip())]
        trailing_spaces = line[len(line.rstrip()):]
        content = line.strip()

        
        chunks = split_text_into_chunks(content, tokenizer)

        translated_chunks = []

        for chunk in chunks:
            translated_chunk = translate_single_text(
                chunk,
                source_lang,
                target_lang,
                tokenizer,
                model,
            )
            translated_chunks.append(translated_chunk)

        translated = " ".join(translated_chunks)

        translated_lines.append(
            leading_spaces + translated.strip() + trailing_spaces
        )

    return "\n".join(translated_lines)