import csv
import statistics
import time
from datetime import datetime
from pathlib import Path

from evaluation_cases import TEST_CASES
from translator import translate_text


def evaluate_translations():
    results = []
    successful_times = []

    print("Iniciando evaluación de TraductorIA...")
    print(f"Casos de prueba: {len(TEST_CASES)}")
    print("La primera traducción puede tardar más en cargar el modelo.\n")

    for index, case in enumerate(TEST_CASES, start=1):
        print(
            f"[{index}/{len(TEST_CASES)}] "
            f"{case['source_lang']} -> {case['target_lang']}"
        )

        start_time = time.perf_counter()

        try:
            translated_text = translate_text(
                case["text"],
                case["source_lang"],
                case["target_lang"],
            )

            elapsed_time = time.perf_counter() - start_time

            status = "OK" if translated_text else "Resultado vacío"

            if translated_text:
                successful_times.append(elapsed_time)

        except Exception as error:
            elapsed_time = time.perf_counter() - start_time
            translated_text = ""
            status = f"ERROR: {error}"

        result = {
            "id": case["id"],
            "source_lang": case["source_lang"],
            "target_lang": case["target_lang"],
            "category": case["category"],
            "original_text": case["text"],
            "reference_translation": case["reference"],
            "model_translation": translated_text,
            "time_seconds": round(elapsed_time, 3),
            "status": status,
        }

        results.append(result)

        print(f"Estado: {status}")
        print(f"Tiempo: {elapsed_time:.2f} segundos")

        if translated_text:
            print(f"Resultado: {translated_text}")

        print("-" * 60)

    if not results:
        print("No hay casos de prueba que evaluar.")
        return

    output_file = (
        Path(__file__).parent
        / f"evaluation_results_{datetime.now():%Y%m%d_%H%M%S}.csv"
    )

    fieldnames = list(results[0].keys())

    with output_file.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    successful = sum(
        result["status"] == "OK"
        for result in results
    )

    print("\n" + "=" * 60)
    print("RESUMEN DE LA EVALUACIÓN")
    print("=" * 60)
    print(f"Casos evaluados: {len(results)}")
    print(f"Traducciones correctas técnicamente: {successful}/{len(results)}")
    print(f"Errores o resultados vacíos: {len(results) - successful}")

    if successful_times:
        print(
            f"Tiempo medio: "
            f"{statistics.mean(successful_times):.2f} segundos"
        )
        print(
            f"Tiempo mediano: "
            f"{statistics.median(successful_times):.2f} segundos"
        )
        print(
            f"Tiempo mínimo: "
            f"{min(successful_times):.2f} segundos"
        )
        print(
            f"Tiempo máximo: "
            f"{max(successful_times):.2f} segundos"
        )

    print(f"\nResultados guardados en: {output_file}")


if __name__ == "__main__":
    evaluate_translations()