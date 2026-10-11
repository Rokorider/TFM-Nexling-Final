
function TranslationPanel({
  type,
  text,
  onTextChange,
  languageName,
  translation,
  loading,
  onClear,
  onCopy,
}) {
  const isSource = type === 'source';

  return (
    <div className={`text-panel ${isSource ? 'source-panel' : 'result-panel'}`}>
      <div className="panel-heading">
        <span>{isSource ? 'Texto original' : 'Traducción'}</span>
        <span className="panel-language">{languageName}</span>
      </div>

      {isSource ? (
        <textarea
          value={text}
          onChange={(e) => onTextChange(e.target.value.slice(0, 5000))}
          placeholder="Escribe aquí el texto que quieres traducir..."
          maxLength={5000}
          aria-label="Texto original"
        />
      ) : (
        <div className="translation-result" aria-live="polite">
          {loading ? (
            <div className="loading-state">
              <span className="spinner" />
              <span>Traduciendo tu texto...</span>
            </div>
          ) : translation ? (
            <p>{translation}</p>
          ) : (
            <p className="placeholder">
              Tu traducción aparecerá aquí...
            </p>
          )}
        </div>
      )}

      <div className="panel-footer">
        {isSource ? (
          <>
            <span>{text.length}/5000 caracteres</span>
            <button className="clear-button" onClick={onClear} type="button">
              Limpiar
            </button>
          </>
        ) : (
          <>
            <span>{translation.length} caracteres</span>
            {translation && (
              <button className="clear-button" onClick={onCopy} type="button">
                Copiar traducción
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default TranslationPanel;
