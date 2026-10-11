import { useEffect, useRef, useState } from 'react';
import './App.css';

import Navbar from './components/Navbar';
import Intro from './components/Intro';
import LanguageSelector, {
  languages,
} from './components/LanguageSelector';
import ChatMessage from './components/ChatMessage';
import TranslationHistory from './components/TranslationHistory';
import Footer from './components/Footer';

import { translateText } from './services/translationService';

function App() {
  const [targetLang, setTargetLang] = useState('es');
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [messages, setMessages] = useState([]);

  const messagesEndRef = useRef(null);

  const [history, setHistory] = useState(() => {
    try {
      const savedHistory = localStorage.getItem(
        'translationHistory'
      );

      return savedHistory ? JSON.parse(savedHistory) : [];
    } catch {
      return [];
    }
  });

  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('traductorTheme') === 'dark';
  });

  useEffect(() => {
    try {
      localStorage.setItem(
        'translationHistory',
        JSON.stringify(history)
      );
    } catch {
      setError('No se ha podido guardar el historial.');
    }
  }, [history]);

  // Desplaza el chat hasta el último mensaje.
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth',
      block: 'end',
    });
  }, [messages, loading]);

  useEffect(() => {
    localStorage.setItem(
      'traductorTheme',
      darkMode ? 'dark' : 'light'
    );
  }, [darkMode]);

  function clearConversation() {
    setMessages([]);
    setText('');
    setError('');
  }

  function restoreTranslation(item) {
    const targetLanguage = languages.find(
      (lang) => lang.name === item.targetName
    );

    if (!targetLanguage) {
      setError(
        'No se ha podido recuperar el idioma de destino.'
      );
      return;
    }

    setTargetLang(targetLanguage.code);
    setText(item.originalText);
    setError('');
  }

  function deleteTranslation(id) {
    setHistory((previousHistory) =>
      previousHistory.filter((item) => item.id !== id)
    );
  }

  function handleTextareaKeyDown(event) {
    if (
      event.key === 'Enter' &&
      !event.shiftKey &&
      !event.nativeEvent.isComposing
    ) {
      event.preventDefault();
      event.currentTarget.form?.requestSubmit();
    }
  }

  async function handleSendMessage(event) {
    event.preventDefault();
    
    if (!text.trim() || loading) {
      return;
    }
  
    const originalText = text.trim();
    const currentTargetLang = targetLang;
    const messageId = `${Date.now()}-${Math.random()}`;
  
    // Mostramos el mensaje original inmediatamente.
    const pendingMessage = {
      id: messageId,
      originalText,
      translatedText: '',
      sourceLang: null,
      targetLang: currentTargetLang,
      sourceName: 'Detectando idioma...',
      targetName:
        languages.find(
          (language) => language.code === currentTargetLang
        )?.name ?? currentTargetLang,
      pending: true,
    };
  
    setMessages((previousMessages) => [
      ...previousMessages,
      pendingMessage,
    ]);
  
    setText('');
    setLoading(true);
    setError('');
  
    try {
      const result = await translateText(
        originalText,
        currentTargetLang
      );
    
      const completedMessage = {
        id: messageId,
        originalText: result.original_text,
        translatedText: result.translated_text,
        sourceLang: result.source_lang,
        targetLang: result.target_lang,
        sourceName: result.source_name,
        targetName: result.target_name,
      };
    
      // Actualizamos el mensaje existente, sin duplicarlo.
      setMessages((previousMessages) =>
        previousMessages.map((message) =>
          message.id === messageId
            ? completedMessage
            : message
        )
      );
    
      setHistory((previousHistory) =>
        [completedMessage, ...previousHistory].slice(0, 20)
      );
    } catch (err) {
      setMessages((previousMessages) =>
        previousMessages.filter(
          (message) => message.id !== messageId
        )
      );
    
      // Recuperamos el texto para que no se pierda.
      setText(originalText);
    
      setError(
        err.message.toLowerCase().includes('fetch')
          ? 'No se puede conectar con el servidor. Comprueba que el backend esté iniciado.'
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  async function copyTranslation(value) {
    try {
      await navigator.clipboard.writeText(value);
    } catch {
      setError('No se ha podido copiar la traducción.');
    }
  }

  return (
    <div className={`app ${darkMode ? 'dark-mode' : ''}`}>
      <Navbar />

      <main className="main-content">
        <Intro />

        <section className="translator">
          <LanguageSelector
            targetLang={targetLang}
            onTargetChange={setTargetLang}
            loading={loading}
          />

          <section className="chat-container">
            <div className="chat-heading">
              <div className="chat-heading-title">
                <h2>Conversación</h2>
                <p>
                  Escribe un mensaje y recibe su traducción.
                </p>
              </div>

              <button
                className="theme-toggle"
                type="button"
                onClick={() => setDarkMode((previous) => !previous)}
                aria-label={
                  darkMode
                    ? 'Activar modo claro'
                    : 'Activar modo oscuro'
                }
                title={
                  darkMode
                    ? 'Cambiar a modo claro'
                    : 'Cambiar a modo oscuro'
                }
              >
                <span aria-hidden="true">
                  {darkMode ? '☀' : '☾'}
                </span>
              </button>

              {messages.length > 0 && (
                <button
                  className="clear-button"
                  type="button"
                  onClick={clearConversation}
                >
                  Nueva conversación
                </button>
              )}
            </div>

            <div
              className="chat-messages"
              aria-live="polite"
            >
              {messages.length === 0 && (
                <div className="chat-empty">
                  <h3>¡Empecemos a traducir!</h3>
                  <p>
                    Escribe un texto en el cuadro inferior
                    para ver el original y su traducción aquí.
                  </p>
                </div>
              )}

              {messages.map((message) => (
                <ChatMessage
                  key={message.id}
                  message={message}
                  onCopy={copyTranslation}
                />
              ))}

              {loading && (
                <div
                  className="chat-loading"
                  role="status"
                  aria-label="Detectando el idioma y traduciendo"
                >
                  <span className="typing-dot"></span>
                  <span className="typing-dot"></span>
                  <span className="typing-dot"></span>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            <form
              className="chat-composer"
              onSubmit={handleSendMessage}
            >
              <textarea
                value={text}
                onChange={(event) =>
                  setText(event.target.value)
                }
                onKeyDown={handleTextareaKeyDown}
                placeholder="Escribe aquí el texto que quieres traducir..."
                rows={3}
                maxLength={5000}
                disabled={loading}
                aria-label="Texto que quieres traducir"
              />

              <div className="chat-composer-footer">
                <span>
                  {text.length}/5000 caracteres
                </span>

                <button
                  className="translate-button"
                  type="submit"
                  disabled={loading || !text.trim()}
                >
                  {loading ? 'Traduciendo...' : 'Enviar'}
                  {!loading && <span>→</span>}
                </button>
              </div>
            </form>
          </section>

          {error && (
            <p className="error-message" role="alert">
              {error}
            </p>
          )}

          <p className="privacy-note">
            Traducción mediante un modelo de inteligencia artificial.
          </p>
        </section>

        <TranslationHistory
          history={history}
          onClearHistory={() => setHistory([])}
          onRestore={restoreTranslation}
          onDelete={deleteTranslation}
        />
      </main>

      <Footer />
    </div>
  );
}

export default App;