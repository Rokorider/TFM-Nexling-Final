
from translator import split_text_into_chunks, load_tokenizer

tokenizer = load_tokenizer()

text = (
    "La inteligencia artificial facilita la comunicación. "
    "Los modelos neuronales permiten traducir textos. "
) * 100

chunks = split_text_into_chunks(
    text,
    tokenizer,
    max_tokens=200,
)

assert len(chunks) > 1, "El texto no se ha dividido."

for index, chunk in enumerate(chunks, start=1):
    tokens = len(
        tokenizer(
            chunk,
            add_special_tokens=False,
        )["input_ids"]
    )

    assert tokens <= 200, (
        f"El fragmento {index} supera el límite: {tokens}"
    )

assert " ".join(chunks).strip() == text.strip(), (
    "Se ha perdido o modificado contenido."
)

print("Todas las pruebas de fragmentación superadas.")
print(f"Fragmentos generados: {len(chunks)}")
