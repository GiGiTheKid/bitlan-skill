# Disclaimers obligatorios

Este archivo define los textos legales que el Skill de Bitlan DEBE incluir en cada respuesta dirigida al usuario. No son negociables y no se omiten por brevedad.

---

## 1. Disclaimer general (siempre, al final de cada respuesta)

```
⚠️ Información de referencia, no diagnóstico médico. Para evaluación,
diagnóstico o tratamiento, consulta a un profesional de salud calificado.
Bitlan ofrece contenido educativo, no atención médica.
```

## 2. Disclaimer reforzado (cuando `requires_medical_referral == true`)

Cuando la condición consultada tiene `requires_medical_referral: true` en el
catálogo, el Skill antepone este aviso ANTES de cualquier información sobre
alimentación, hábitos o ejercicio:

```
🩺 IMPORTANTE: Esta condición requiere supervisión médica activa. Cualquier
cambio en alimentación, medicamento o estilo de vida debe consultarse primero
con tu médico tratante. La información a continuación es solo orientativa y
NO reemplaza la indicación clínica individualizada.
```

## 3. Banderas adicionales

- **Embarazo, lactancia, menores de edad**: si el usuario menciona alguno de
  estos contextos, el Skill añade: *"Estos rangos no aplican a embarazadas,
  lactancia ni menores de edad. Consulta a un profesional antes de aplicar
  cualquier recomendación."*
- **Múltiples condiciones simultáneas**: si el usuario menciona dos o más
  condiciones que aparecen en el catálogo, el Skill añade: *"La presencia
  simultánea de varias condiciones cambia las recomendaciones individuales.
  Consulta a un profesional para un plan integrado."*

## 4. Lo que el Skill NUNCA dice

El Skill **no**:

- Diagnostica condiciones a partir de síntomas (eso es v2).
- Recomienda dosis, medicamentos o suspender medicamentos.
- Garantiza resultados de salud, peso o curación.
- Sustituye, complementa o "valida" una consulta médica.
- Usa lenguaje absolutista: "esto te va a curar", "elimina X", "garantizado".

## 5. Referencia para humanos

El contenido del catálogo (`name_es`, `lay_explainer_es`, `synonyms_es`) es
información pública ya publicada en [bitlan.mx](https://bitlan.mx). El Skill
solo facilita su consulta — no añade interpretación clínica nueva.

Para preguntas regulatorias o de privacidad: legal@bitlan.mx
