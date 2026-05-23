# Bitlan Skill

> **Bitlan — Tu cuerpo tiene un código. Te ayudamos a interpretarlo.**

Claude Skill que conecta con el catálogo público de condiciones médicas de [Bitlan](https://bitlan.mx) y devuelve fichas curadas en español: explicación en lenguaje plano, prevalencia en México, bandera de supervisión médica y link al plan personalizado (alimentos, lista de compras, hábitos, ejercicio, sueño) en bitlan.mx.

Diseñado para personas en LATAM que quieren información confiable sobre una condición específica antes de tomar decisiones de alimentación o estilo de vida.

---

## Instalación

### Como Claude Skill (Cowork / Claude Code)

1. Clona el repo:
   ```bash
   git clone https://github.com/GiGiTheKid/bitlan-skill.git
   cd bitlan-skill
   ```
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Cárgalo en Claude apuntando a `SKILL.md`.

### Como herramienta CLI standalone

```bash
git clone https://github.com/GiGiTheKid/bitlan-skill.git
cd bitlan-skill
pip install -r requirements.txt
python scripts/lookup.py "diabetes"
```

---

## Uso

```bash
# Lookup por nombre o sinónimo
python scripts/lookup.py "diabetes"
python scripts/lookup.py "tiroides baja"
python scripts/lookup.py "SOP"
python scripts/lookup.py "azucar alta"

# Listar catálogo completo
python scripts/lookup.py --list

# Lookup directo por slug
python scripts/lookup.py --slug diabetes_t2

# Forzar refresh (ignora cache local)
python scripts/lookup.py --refresh "prediabetes"
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
- Disclaimer médico al final de cada respuesta.
- Disclaimer reforzado cuando la condición requiere supervisión médica activa.

**No hace:**
- No diagnostica a partir de síntomas (eso vendrá en v0.3 con disclaimer reforzado).
- No recomienda dosis, medicamentos ni suspender tratamiento.
- No reemplaza atención médica profesional.

---

## Arquitectura

```
bitlan-skill/
├── SKILL.md                    # Manifest del Skill (descripción + triggers)
├── scripts/
│   └── lookup.py              # Wrapper Python con cache y fuzzy match
├── reference/
│   ├── catalog-sample.json    # Snapshot del shape de la API
│   └── disclaimers.md         # Texto legal obligatorio
├── tests/
│   └── test_lookup.py         # Unit + smoke tests
├── .github/workflows/
│   └── test.yml               # CI: tests en cada push
├── requirements.txt
├── requirements-dev.txt
├── LICENSE                     # MIT
└── README.md
```

**Endpoint**: `GET https://bitlan.mx/api/medical-conditions/catalog` (sin auth, RLS público).

---

## Desarrollo

```bash
# Setup
pip install -r requirements-dev.txt

# Tests unitarios (sin red)
pytest tests/test_lookup.py -v -k "not TestLiveAPI"

# Tests con red (golpea la API en vivo)
pytest tests/test_lookup.py -v
```

---

## Roadmap

- **v0.1.0** (actual) — Lookup por nombre/sinónimo + fuzzy match + cache local.
- **v0.2.0** — Comando `--related` para condiciones relacionadas por categoría / overlap.
- **v0.3.0** — Symptom Navigator: descripción de síntoma → 2-3 condiciones candidatas con disclaimer reforzado.

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
