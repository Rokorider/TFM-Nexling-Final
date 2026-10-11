const API_URL = 'http://127.0.0.1:8000';

async function request(endpoint, body) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || 'No se ha podido completar la petición.'
    );
  }

  return data;
}

export async function translateText(text, targetLang) {
  return request('/translate', {
    text,
    target_lang: targetLang,
  });
}

export async function detectLanguage(text) {
  return request('/detect-language', { text });
}