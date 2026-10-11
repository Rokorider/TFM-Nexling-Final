const languages = [
  { code: 'es', name: 'Español' },
  { code: 'en', name: 'Inglés' },
  { code: 'fr', name: 'Francés' },
  { code: 'de', name: 'Alemán' },
  { code: 'it', name: 'Italiano' },
  { code: 'pt', name: 'Portugués' },
  { code: 'nl', name: 'Neerlandés' },
  { code: 'ru', name: 'Ruso' },
  { code: 'zh', name: 'Chino simplificado' },
  { code: 'ja', name: 'Japonés' },
];

function LanguageSelector({
  targetLang,
  onTargetChange,
  loading,
}) {
  return (
    <div className="language-bar">
      <div className="language-selector">
        <label htmlFor="target-language">
          Traducir a
        </label>

        <select
          id="target-language"
          value={targetLang}
          onChange={(event) =>
            onTargetChange(event.target.value)
          }
          disabled={loading}
        >
          {languages.map((language) => (
            <option
              key={language.code}
              value={language.code}
            >
              {language.name}
            </option>
          ))}
        </select>
      </div>

      <p className="language-detection-note">
        El idioma original se detecta automáticamente.
      </p>
    </div>
  );
}

export { languages };
export default LanguageSelector;