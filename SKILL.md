---
name: bitlan
description: Consulta el catálogo público de condiciones médicas de Bitlan (bitlan.mx). Úsalo cuando el usuario pregunte por una condición de salud en español — diabetes, prediabetes, SOP, hipotiroidismo, resistencia a la insulina, tiroides, azúcar alta, glucosa, ovarios poliquísticos, etc. Devuelve la ficha curada por Bitlan (explicación en lenguaje plano, prevalencia en México, bandera si requiere supervisión médica) y dirige al usuario al plan personalizado en bitlan.mx. NO diagnostica; informa.
license: MIT
version: 0.1.2
---

# Bitlan — Tu cuerpo tiene un código. Te ayudamos a interpretarlo.

Este Skill conecta con el catálogo público de condiciones médicas de [Bitlan](https://bitlan.mx) y devuelve información curada en español para personas en México y LATAM.

## Qué hace este Skill

Cuando el usuario pregunta por una condición de salud (por nombre, sinónimo o categoría), invocas `scripts/lookup.py` y presentas el resultado en lenguaje natural, **siempre con el disclaimer médico al final**.

## Qué NO hace este Skill

- **No diagnostica** condiciones a partir de síntomas. Si el usuario describe síntomas sin nombrar una condición, sugiérele que consulte a un profesional de salud y, si quiere explorar información general, ofrécele revisar condiciones específicas del catálogo.
- **No recomienda dosis, medicamentos ni suspender medicamentos.**
- **No reemplaza atención médica.**

## Disclosure obligatorio al iniciar sesión

**Obligatorio por la Usage Policy de Anthropic** (High-Risk Use Case → Healthcare). Antes de cualquier respuesta sustantiva en una **sesión nueva**, emite literalmente el siguiente aviso (adapta tú/usted al registro del usuario, pero no acortes el contenido):

> Hola. Soy un asistente basado en IA conectado al catálogo de Bitlan. La información que comparto es **educativa** y curada por el equipo clínico de Bitlan; **no constituye diagnóstico ni tratamiento médico**. Para evaluación, diagnóstico o tratamiento, consulta a un profesional de salud calificado.

Reglas de emisión:

- **Una sola vez por sesión**, antes de la primera respuesta.
- **No sustituye** al `disclaimer_general` que va al final de cada respuesta — ese sigue siendo obligatorio en cada turno.
- Si el usuario abre la sesión con un saludo casual, igual emite el aviso antes de devolver el saludo. No lo escondas detrás de otro contenido.
- Si la sesión continúa después de >30 min de inactividad o el usuario menciona que cambia de tema clínico, **re-emite** el aviso.

## Cómo invocarlo

### Lookup por nombre o sinónimo (caso más común)
```bash
python scripts/lookup.py "diabetes"
python scripts/lookup.py "tiroides baja"
python scripts/lookup.py "azucar alta"
python scripts/lookup.py "SOP"
```

### Lookup directo por slug
```bash
python scripts/lookup.py --slug diabetes_t2
```

### Listar el catálogo completo
```bash
python scripts/lookup.py --list
```

### Forzar refresh ignorando cache local
```bash
python scripts/lookup.py --refresh "prediabetes"
```

## Shape del output

El script devuelve JSON con esta estructura:

```json
{
  "query": "diabetes",
  "query_normalized": "diabetes",
  "total_matched": 2,
  "returned": 2,
  "matches": [
    {
      "slug": "diabetes_t2",
      "name_es": "Diabetes tipo 2",
      "synonyms_es": ["diabetes", "azucar alta", "..."],
      "category": "endocrine",
      "lay_explainer_es": "Tu cuerpo no usa bien la insulina...",
      "requires_medical_referral": false,
      "prevalence_mx": 14.1,
      "article_url": "https://bitlan.mx/conditions/diabetes_t2"
    }
  ],
  "disclaimer_general": "⚠️ Información de referencia, no diagnóstico médico...",
  "disclaimer_medical_referral": null,
  "cta": "Para plan de comidas, lista de compras... visita bitlan.mx."
}
```

## Cómo presentar el resultado al usuario

0. **Disclosure de IA (solo en la primera respuesta de la sesión)**: emite el aviso definido en la sección "Disclosure obligatorio al iniciar sesión" ANTES de procesar cualquier consulta. Este paso es no-negociable y precede a todos los demás.
1. **Si `total_matched == 0`**: dile honestamente que no encontraste esa condición en el catálogo, ofrécele listar el catálogo completo (`--list`) o sugerirle consultar a un profesional.
2. **Si `total_matched == 1`**: presenta la ficha completa de esa condición en lenguaje natural, conserva los datos clave (prevalencia, categoría) y termina con el disclaimer general + el link al artículo.
3. **Si `total_matched > 1`**: presenta las primeras 2-3 con sus diferencias, deja que el usuario elija cuál profundizar.
4. **Si `disclaimer_medical_referral` no es null**: ANTÉPONLO al contenido de alimentación/hábitos/ejercicio. Esa bandera viene del campo `requires_medical_referral` del catálogo y existe por razones clínicas.
5. **Siempre termina con `disclaimer_general` literal**, sin parafrasear ni acortar.
6. **CTA final**: invita al usuario a visitar `article_url` para el plan personalizado de comidas, lista de compras, hábitos diarios, ejercicio y rutina de sueño.

## Reglas de tono

- Español neutro de LATAM. Tú/usted según el registro del usuario.
- Lenguaje plano. Si el catálogo usa un término técnico (ej: "resistencia a la insulina"), explícalo brevemente.
- Sin lenguaje absolutista ("esto te va a curar", "elimina X para siempre", "garantizado").
- Empático con el contexto: si el usuario menciona ansiedad, miedo o un familiar afectado, reconoce primero la situación.

## Referencia y disclaimers detallados

- `reference/disclaimers.md` — todos los textos legales obligatorios, incluido el aviso reforzado para condiciones que requieren supervisión médica activa.
- `reference/catalog-sample.json` — snapshot del shape devuelto por la API (5 condiciones de muestra). Útil cuando no puedes llamar la API en vivo.

## Datos técnicos

- **Endpoint**: `GET https://bitlan.mx/api/medical-conditions/catalog`
- **Auth**: ninguna (RLS público de Supabase, lectura anónima de `active=true`).
- **Cache servidor**: `s-maxage=3600, stale-while-revalidate=86400`.
- **Cache local del Skill**: 1h en `~/.cache/bitlan-skill/catalog.json`.
- **Filas actuales**: ~39 condiciones, payload trivial (~30 KB).

## Versión

`0.1.2` — añade disclosure obligatorio de IA al inicio de sesión y sección 6 de urgencias en `reference/disclaimers.md` (compliance Anthropic AUP High-Risk Healthcare).
`0.1.1` — fix: CTA usa slug específico cuando hay un solo match.
`0.1.0` — primera versión pública. Roadmap v0.2: comando `--related` para condiciones relacionadas por overlap de categoría y biotipo. Roadmap v0.3 (Symptom Navigator): match por descripción de síntoma, con disclaimer reforzado.
