
from translator import split_text_into_chunks, load_tokenizer

tokenizer = load_tokenizer()

test_cases = {
    "Español": (
        "La inteligencia artificial facilita la comunicación. "
        "Los modelos neuronales permiten traducir textos. "
    ) * 100,
    
    

    "Inglés": (
        "Artificial intelligence helps people communicate. "
        "Neural models can translate text between languages. "
    ) * 100,

    "Chino": (
        "人工智能正在改变我们的生活。"
        "机器翻译帮助人们交流。"
    ) * 100,

    "Japonés": (
        "人工知能は私たちの生活を変えています。"
        "機械翻訳は言語の壁を越える助けになります。"
    ) * 100,

    "Palabra larga": "supercalifragilisticoespialidoso" * 100,
}


MAX_TOKENS = 200

for language, text in test_cases.items():
    chunks = split_text_into_chunks(
        text,
        tokenizer,
        max_tokens=MAX_TOKENS,
    )

    assert chunks, f"{language}: no se generaron fragmentos"

    for index, chunk in enumerate(chunks, start=1):
        token_count = len(
            tokenizer(
                chunk,
                add_special_tokens=False,
            )["input_ids"]
        )

        assert token_count <= MAX_TOKENS, (
            f"{language}: fragmento {index} tiene "
            f"{token_count} tokens"
        )
    reconstructed_text = "".join(chunks)

    assert reconstructed_text == text, (
        f"{language}: el texto original no se ha conservado"
    )

    print(
        f"OK - {language}: {len(chunks)} fragmentos, "
        "contenido conservado"
    )

    print(
        f"OK - {language}: {len(chunks)} fragmentos"
    )

print("\nTodas las pruebas superadas.")
