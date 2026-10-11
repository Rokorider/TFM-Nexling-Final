function TranslationHistory({
  history,
  onClearHistory,
  onRestore,
  onDelete,
}) {
  if (history.length === 0) {
    return null;
  }

  return (
    <section className="history-section">
      <div className="history-heading">
        <h2>Historial de traducciones</h2>

        <button
          className="clear-button"
          onClick={onClearHistory}
          type="button"
        >
          Borrar historial
        </button>
      </div>

      <div className="history-list">
        {history.map((item) => (
          <article className="history-item" key={item.id}>
            <div className="history-languages">
              {item.sourceName} → {item.targetName}
            </div>

            <p>
              <strong>Original:</strong> {item.originalText}
            </p>

            <p>
              <strong>Traducción:</strong> {item.translatedText}
            </p>

            <div className="history-actions">
              <button
                className="clear-button"
                onClick={() => onRestore(item)}
                type="button"
              >
                Recuperar traducción
              </button>

              <button
                className="delete-history-button"
                onClick={() => onDelete(item.id)}
                type="button"
                aria-label="Eliminar esta traducción del historial"
              >
                Eliminar
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default TranslationHistory;