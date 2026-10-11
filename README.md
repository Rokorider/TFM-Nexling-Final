# Chatbot de Traducción Multilingüe con Inteligencia Artificial

Aplicación web desarrollada como **Trabajo Fin de Máster en Inteligencia Artificial, Machine Learning e Ingeniería de la Información**.

El proyecto consiste en un sistema de traducción automática multilingüe que utiliza un modelo neuronal basado en la arquitectura Transformer. Su objetivo es facilitar la traducción de textos entre diferentes idiomas mediante una interfaz web sencilla, intuitiva y de tipo conversacional.

La aplicación integra el modelo **NLLB-200 Distilled 600M**, desarrollado por Meta y disponible en Hugging Face, con un backend en Python y una interfaz desarrollada con React.

## Características principales

- Traducción automática entre diez idiomas: español, inglés, francés, alemán, italiano, portugués, neerlandés, ruso, chino y japonés.
- Detección automática del idioma de origen.
- Selección manual de los idiomas de origen y destino.
- Interfaz conversacional para visualizar las traducciones.
- Historial de traducciones con opciones de consulta y eliminación.
- Validación de entradas y gestión de errores.
- Conservación de saltos de línea en los textos traducidos.

## Tecnologías utilizadas

### Frontend
- **React:** desarrollo de la interfaz de usuario.
- **Vite:** entorno de desarrollo y compilación.
- **JavaScript, HTML y CSS:** implementación de la lógica y el diseño visual.

### Backend
- **Python:** lenguaje principal del servidor.
- **FastAPI:** desarrollo de la API REST.
- **Pydantic:** validación de las solicitudes.
- **Uvicorn:** servidor ASGI para ejecutar la aplicación.
- **fast-langdetect:** detección automática de idiomas.

### Inteligencia artificial
- **Hugging Face Transformers:** carga y utilización del modelo neuronal.
- **PyTorch:** ejecución de las operaciones de inferencia.
- **facebook/nllb-200-distilled-600M:** modelo multilingüe de traducción automática.

## Estructura del proyecto

```text
TFM/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── backend/
│   ├── main.py
│   ├── translator.py
│   ├── language_detector.py
│   ├── evaluation_cases.py
│   ├── evaluate_translations.py
│   ├── test_robustness.py
│   └── ...
├── .gitignore
└── README.md
```

## Requisitos previos

Para ejecutar la aplicación en un equipo local es necesario disponer de:

- **Python 3.13**, versión utilizada durante el desarrollo.
- **Node.js y npm**, para ejecutar el frontend.
- **Git**, para clonar el repositorio.
- Conexión a Internet durante la instalación y la primera descarga del modelo.
- Espacio de almacenamiento y memoria RAM suficientes para ejecutar el modelo neuronal.

La aplicación puede ejecutarse localmente utilizando CPU, aunque el rendimiento dependerá de las características del equipo.

## Instalación y ejecución

### 1. Clonar el repositorio

Abrir una terminal y ejecutar:

```bash
git clone https://github.com/TU_USUARIO/NOMBRE_REPOSITORIO.git
cd NOMBRE_REPOSITORIO
```

Sustituir la URL por la dirección real del repositorio.

### 2. Configurar el backend

Acceder a la carpeta del backend:

```bash
cd backend
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Windows mediante PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias del proyecto:

```bash
python -m pip install -r requirements.txt
```

El archivo `requirements.txt` debe contener las dependencias necesarias para ejecutar el backend.

### 3. Iniciar el servidor

Desde la carpeta `backend`, con el entorno virtual activado:

```bash
python -m uvicorn main:app --reload
```

El servidor se iniciará en:

http://127.0.0.1:8000

La documentación interactiva de la API estará disponible en:

http://127.0.0.1:8000/docs

**Nota:** durante la primera ejecución que requiera el modelo, Hugging Face descargará sus archivos. Este proceso puede tardar varios minutos dependiendo de la conexión a Internet.

### 4. Configurar el frontend

Abrir una segunda terminal y acceder a la carpeta `frontend`:

```bash
cd frontend
```

Instalar las dependencias:

```bash
npm install
```

Iniciar el servidor de desarrollo:

```bash
npm run dev
```

La aplicación estará disponible normalmente en:

http://localhost:5173

Es necesario mantener ejecutándose tanto el backend como el frontend para utilizar el sistema.

## Funcionamiento

1. Acceder a la aplicación desde el navegador.
2. Seleccionar el idioma de destino.
3. Elegir manualmente el idioma de origen o utilizar la detección automática.
4. Introducir el texto que se desea traducir.
5. Enviar la solicitud de traducción.
6. Consultar el resultado generado en la interfaz conversacional.

El frontend envía la solicitud al backend mediante HTTP. FastAPI valida los datos, determina el idioma de origen cuando es necesario y utiliza el modelo NLLB para generar la traducción.

Una vez completado el procesamiento, el resultado se devuelve al frontend y se muestra al usuario.

## Pruebas y evaluación

El proyecto incluye archivos destinados a comprobar el funcionamiento y rendimiento del sistema:

- `evaluation_cases.py`: conjunto de quince casos de traducción.
- `evaluate_translations.py`: ejecución de las pruebas y registro de resultados en CSV.
- `test_robustness.py`: comprobación de entradas incorrectas y otros escenarios de funcionamiento.

Para ejecutar las pruebas de evaluación desde el directorio `backend`:

```bash
python evaluate_translations.py
```

Para ejecutar las pruebas de robustez:

```bash
python test_robustness.py
```

Durante la evaluación se compararon diferentes configuraciones de generación del modelo. La configuración final obtuvo un tiempo medio aproximado de **1,93 segundos por traducción** en los quince casos evaluados, frente a los 4,55 segundos de la configuración inicial.

Estos resultados corresponden al entorno de pruebas utilizado durante el desarrollo y pueden variar en otros equipos.

## Limitaciones

- La calidad de las traducciones puede variar según el idioma, el contexto y la complejidad del texto.
- Las expresiones breves o ambiguas pueden generar resultados imprecisos.
- El modelo necesita recursos de memoria y procesamiento para ejecutarse localmente.
- La traducción de líneas independientes puede reducir el contexto disponible para el modelo.
- El sistema no dispone de un mecanismo de aprendizaje continuo a partir de las correcciones de los usuarios.

## Autor

Trabajo Fin de Máster en Inteligencia Artificial, Machine Learning e Ingeniería de la Información.

## Finalidad del proyecto

Este proyecto tiene una finalidad académica y demostrativa. Su desarrollo permite aplicar conocimientos de Procesamiento del Lenguaje Natural, modelos Transformer, integración de sistemas de inteligencia artificial y desarrollo de aplicaciones web.