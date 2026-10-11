from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from language_detector import detect_language
from translator import LANGUAGES, translate_text

app = FastAPI(
    title="TraductorIA API",
    description="API para traducción automática mediante inteligencia artificial.",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslationRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    target_lang: str
    source_lang: str | None = None


class LanguageDetectionRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de TraductorIA",
        "estado": "funcionando",
    }


@app.get("/health")
def comprobar_estado():
    return {"estado": "ok"}


@app.get("/languages")
def obtener_idiomas():
    return {
        code: language["name"]
        for code, language in LANGUAGES.items()
    }


@app.post("/detect-language")
def detectar_idioma(request: LanguageDetectionRequest):
    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=422,
            detail="El texto no puede estar vacío.",
        )

    language = detect_language(text)

    if language is None:
        raise HTTPException(
            status_code=422,
            detail=(
                "No se ha podido identificar un idioma admitido. "
                "Prueba con un texto más largo."
            ),
        )

    return {
        "language": language,
        "name": LANGUAGES[language]["name"],
    }


@app.post("/translate")
def traducir(request: TranslationRequest):
    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=422,
            detail="El texto no puede estar vacío.",
        )

    if request.target_lang not in LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail="El idioma de destino no está admitido.",
        )

    # Si no se especifica el idioma de origen, lo detectamos.
    if request.source_lang is None:
        source_lang = detect_language(text)

        if source_lang is None:
            raise HTTPException(
                status_code=422,
                detail=(
                    "No se ha podido identificar un idioma admitido. "
                    "Prueba con un texto más largo."
                ),
            )
    else:
        source_lang = request.source_lang

        if source_lang not in LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail="El idioma de origen no está admitido.",
            )

    try:
        translation = translate_text(
            text,
            source_lang,
            request.target_lang,
        )

        return {
            "original_text": text,
            "translated_text": translation,
            "source_lang": source_lang,
            "source_name": LANGUAGES[source_lang]["name"],
            "target_lang": request.target_lang,
            "target_name": LANGUAGES[request.target_lang]["name"],
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"No se ha podido realizar la traducción: {error}",
        ) from error