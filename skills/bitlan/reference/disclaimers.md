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

## 6. Disclaimer de urgencias y derivación

**Filosofía:** este es un disclaimer, **no un bloqueo**. La ficha solicitada
SIEMPRE se entrega al usuario. Lo único que cambia cuando el contexto sugiere
una urgencia es que ANTES de la ficha se antepone el aviso de derivación con
los teléfonos de emergencia. El usuario decide qué hacer con esa información.

### 6.1 Señales de urgencia que disparan el disclaimer

El Skill antepone el aviso reforzado (sección 6.3) cuando el mensaje del
usuario, además de pedir información sobre una condición, menciona alguna de
las siguientes señales:

- **Cardiovasculares**: dolor opresivo en el pecho, dolor que irradia a brazo
  izquierdo / mandíbula / espalda, dificultad respiratoria súbita,
  desmayo / pérdida de consciencia, palpitaciones acompañadas de mareo.
- **Neurológicas**: pérdida súbita de fuerza o sensibilidad en una mitad del
  cuerpo, dificultad para hablar o entender, asimetría facial nueva, dolor de
  cabeza súbito e intensísimo ("el peor de mi vida"), convulsiones.
- **Metabólicas agudas en diabetes**: glucosa medida muy alta o muy baja con
  síntomas, vómito persistente, aliento afrutado, somnolencia inusual.
- **Hemorrágicas o de shock**: sangrado abundante no controlado, palidez
  extrema, sudoración fría con confusión.
- **Obstétricas urgentes**: sangrado abundante en embarazo, ausencia
  prolongada de movimientos fetales, cefalea + visión borrosa + hinchazón en
  el último trimestre.
- **Pediátricas**: fiebre alta en lactante menor de 3 meses, deshidratación
  marcada, dificultad respiratoria, decaimiento extremo.

Lista no exhaustiva. Si el Skill detecta lenguaje compatible con urgencia
aunque no esté listado arriba, opera con el mismo criterio: antepone el aviso
y entrega la ficha.

### 6.2 Teléfonos de emergencia y derivación (México)

| Recurso | Número | Cuándo |
|---|---|---|
| Emergencias generales | **911** | Cualquier urgencia médica activa |
| Cruz Roja Mexicana | **065** | Ambulancia, soporte prehospitalario |
| Línea de la Vida (SSA) | **800-290-0024** | Crisis emocional, salud mental, uso de sustancias |
| SAPTEL | **55-5259-8121** | Apoyo psicológico telefónico 24/7 |
| Locatel CDMX | **55-5658-1111** | Orientación médica y psicológica, CDMX |

Fuera de México, el Skill no enumera teléfonos locales; en ese caso se limita
a sugerir: *"Marca el número de emergencias de tu país o acude al servicio
de urgencias más cercano."*

### 6.3 Texto del aviso (cuando aplica)

```
🚨 IMPORTANTE — Si lo que describes corresponde a una urgencia médica
activa, no esperes: marca el 911 o acude al servicio de urgencias más
cercano. Si la urgencia es emocional o de salud mental, marca la Línea
de la Vida 800-290-0024 (24/7, gratuito).

La información que sigue es educativa y NO sustituye atención médica
inmediata. Está disponible para ti igualmente porque entendemos que
quizá quieras leerla en otro momento o compartirla con un familiar.
```

A continuación, el Skill entrega la ficha completa de la condición consultada
con el flujo normal (disclaimer general al final, disclaimer reforzado si
aplica, CTA al artículo).

### 6.4 Casos donde el Skill se aparta de "puro disclaimer"

Una sola excepción al patrón "disclaimer + ficha siempre": si el usuario
expresa **ideación activa de suicidio, intención de autolesión o de daño a
otros**, el Skill prioriza la derivación a Línea de la Vida (800-290-0024) /
SAPTEL (55-5259-8121) y NO entrega ficha de catálogo en ese turno. Una vez
que el usuario indica que está acompañado o en lugar seguro, el Skill puede
ofrecer la información solicitada en el siguiente turno.

Esta excepción no aplica cuando el usuario pregunta por una condición de
salud mental (depresión, ansiedad, etc.) sin expresar ideación activa — en
ese caso se opera con el patrón normal: disclaimer + ficha.

### 6.5 Lo que el Skill NO hace en urgencias

- No diagnostica si lo que describe el usuario "es o no" una urgencia.
- No estima gravedad, probabilidad ni tiempo de evolución clínica.
- No sustituye la valoración del 911, de un médico de urgencias o de la
  línea de crisis.
- No retiene información que el usuario ya pidió explícitamente.
