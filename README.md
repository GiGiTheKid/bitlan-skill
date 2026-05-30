# Bitlan Skill

> **Bitlan — Tu cuerpo tiene un código. Te ayudamos a interpretarlo.**

Claude **plugin** que conecta con el catálogo público de condiciones médicas de [Bitlan](https://bitlan.mx) y devuelve fichas curadas en español: explicación en lenguaje plano, prevalencia en México, bandera de supervisión médica y link al plan personalizado (alimentos, lista de compras, hábitos, ejercicio, sueño) en bitlan.mx.

Diseñado para personas en LATAM que quieren información confiable sobre una condición específica antes de tomar decisiones de alimentación o estilo de vida.

> **Nota de privacidad:** la query del usuario se procesa localmente — el skill descarga el catálogo público de Bitlan y filtra del lado del cliente. La pregunta del usuario **no se transmite** al servidor de Bitlan.

---

## Instalación

### Como plugin de Claude Code / Cowork (recomendado)

Una vez listado en el [Anthropic plugin marketplace](https://clau.de/plugin-directory-submission):

```
/plugin install bitlan@claude-plugins-community
```

Mientras tanto, puedes registrar este repo como marketplace local:

```
/plugin marketplace add GiGiTheKid/bitlan-skill
/plugin install bitlan@bitlan-skill
```

### Como herramienta CLI standalone

```bash
git clone https://github.com/GiGiTheKid/bitlan-skill.git
cd bitlan-skill
python3 skills/bitlan/scripts/lookup.py "diabetes"
```

> **Zero-deps:** el script usa solo la stdlib de Python 3.10+. No requiere `pip install`.

---

## Uso

```bash
# Lookup por nombre o sinónimo
python3 skills/bitlan/scripts/lookup.py "diabetes"
python3 skills/bitlan/scripts/lookup.py "tiroides baja"
python3 skills/bitlan/scripts/lookup.py "SOP"
python3 skills/bitlan/scripts/lookup.py "azucar alta"

# Listar catálogo completo
python3 skills/bitlan/scripts/lookup.py --list

# Lookup directo por slug
python3 skills/bitlan/scripts/lookup.py --slug diabetes_t2

# Forzar refresh (ignora cache local)
python3 skills/bitlan/scripts/lookup.py --refresh "prediabetes"
```

### Ejemplo de output

```json
{
  "query": "tiroides baja",
  "query_normalized": "tiroides baja",
  "total_matched": 1,
  "returned": 1,
  "matches": [
    {
      "slug": "hipotiroidismo",
      "name_es": "Hipotiroidismo",
      "synonyms_es": ["tiroides baja", "tiroides lenta"],
      "category": "endocrine",
      "lay_explainer_es": "Tu glándula tiroides produce menos hormonas de lo necesario. Suele tratarse con levotiroxina.",
      "requires_medical_referral": false,
      "prevalence_mx": null,
      "article_url": "https://bitlan.mx/conditions/hipotiroidismo"
    }
  ],
  "disclaimer_general": "⚠️ Información de referencia, no diagnóstico médico...",
  "cta": "Para plan de comidas, lista de compras... visita bitlan.mx."
}
```

---

## Qué hace y qué NO hace

**Hace:**
- Búsqueda fuzzy (sin acentos, case-insensitive) sobre nombre y sinónimos.
- Cache local 1h alineado con `s-maxage=3600` del servidor.
- **Disclosure obligatorio de IA al inicio de cada sesión** (cumplimiento Anthropic AUP High-Risk Healthcare).
- Disclaimer médico al final de cada respuesta.
- Disclaimer reforzado cuando la condición requiere supervisión médica activa.
- Aviso de urgencias con teléfonos MX (911, Línea de la Vida, SAPTEL, Locatel) cuando el mensaje del usuario sugiere urgencia clínica.

**No hace:**
- No diagnostica a partir de síntomas (eso vendrá en v0.3 con disclaimer reforzado).
- No recomienda dosis, medicamentos ni suspender tratamiento.
- No reemplaza atención médica profesional.
- **No transmite la query del usuario al servidor de Bitlan** — el filtrado es local.

---

## Arquitectura

```
bitlan-skill/
├── .claude-plugin/
│   └── plugin.json              # Manifest del plugin
├── skills/
│   └── bitlan/
│       ├── SKILL.md             # Manifest del skill (descripción + triggers)
│       ├── scripts/
│       │   └── lookup.py        # Wrapper Python con cache y fuzzy match
│       ├── reference/
│       │   ├── catalog-sample.json    # Snapshot del shape de la API
│       │   ├── disclaimers.md         # Textos legales obligatorios + sección 6 urgencias
│       │   └── medical-review.md      # Declaración de revisión clínica (AUP HIL)
│       └── tests/
│           └── test_lookup.py   # Unit + smoke tests
├── .github/workflows/
│   └── test.yml                 # CI: tests en cada push + smoke diario
├── requirements.txt
├── requirements-dev.txt
├── LICENSE                       # MIT
└── README.md
```

**Endpoint**: `GET https://bitlan.mx/api/medical-conditions/catalog` (sin auth, RLS público).

---

## Cumplimiento (Anthropic Usage Policy)

Bitlan opera bajo High-Risk Use Case → Healthcare. Documentado en:

- `skills/bitlan/SKILL.md` — sección "Disclosure obligatorio al iniciar sesión".
- `skills/bitlan/reference/disclaimers.md` — secciones 1–6 (incluye protocolo de urgencias).
- `skills/bitlan/reference/medical-review.md` — declaración pública de Human-in-the-loop.

---

## Desarrollo

```bash
# Setup
pip install -r requirements-dev.txt

# Tests unitarios (sin red)
pytest skills/bitlan/tests/test_lookup.py -v -k "not TestLiveAPI"

# Tests con red (golpea la API en vivo)
pytest skills/bitlan/tests/test_lookup.py -v
```

---

## Roadmap

- **v0.2.0** (actual) — Layout de plugin (`.claude-plugin/plugin.json`, `skills/bitlan/`), cumplimiento Anthropic AUP completo.
- **v0.3.0** — Comando `--related` para condiciones relacionadas por categoría / overlap.
- **v0.4.0** — Symptom Navigator: descripción de síntoma → 2-3 condiciones candidatas con disclaimer reforzado.

---

## Sobre Bitlan

Bitlan ofrece plan de comidas personalizado, lista de compras categorizada, hábitos diarios, rutina de ejercicio y plan de sueño basados en tu perfil de salud. El Skill es la puerta de entrada al producto: identifica tu condición, después visita [bitlan.mx](https://bitlan.mx) para el plan accionable.

---

## License

MIT. Ver [LICENSE](./LICENSE).

## Contribuir

PRs bienvenidos, especialmente para:
- Mejoras en fuzzy match (synonyms adicionales, mejor handling de plurales).
- Tests adicionales.
- Documentación en otros idiomas.

Para issues regulatorios o de privacidad: legal@bitlan.mx
