function ChatMessage({ message, onCopy }) {
  return (
    <article className="chat-message">
      <div className="chat-message-original">
        <div className="chat-message-label">
          Original · {message.sourceName}
        </div>

        <p style={{ whiteSpace: 'pre-line' }}>
          {message.originalText}
        </p>
      </div>

      {!message.pending && message.translatedText && (
        <div className="chat-message-translation">
          <div className="chat-message-label">
            Traducción · {message.targetName}
          </div>

          <p style={{ whiteSpace: 'pre-line' }}>
            {message.translatedText}
          </p>

          <button
            className="clear-button"
            type="button"
            onClick={() => onCopy(message.translatedText)}
          >
            Copiar traducción
          </button>
        </div>
      )}
    </article>
  );
}

export default ChatMessage;