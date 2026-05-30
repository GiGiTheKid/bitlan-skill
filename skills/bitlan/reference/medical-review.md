# Revisión clínica del catálogo

Este archivo declara públicamente quién y cómo revisa el contenido médico del catálogo de Bitlan. Existe para cumplir con el requisito de **Human-in-the-loop** definido en la [Usage Policy de Anthropic](https://www.anthropic.com/legal/aup) para casos de uso de salud (High-Risk Use Case → Healthcare).

> **Filosofía:** preferimos un stub honesto que declara el estado real de la curación a inventar credenciales que no existen.

---

## 1. Estado actual de la revisión clínica

**Bitlan opera en `v0.1.2` sin un revisor médico colegiado formal en plantilla.** El contenido del catálogo (`name_es`, `synonyms_es`, `lay_explainer_es`, `requires_medical_referral`, `prevalence_mx`) lo curan los responsables del producto basándose en fuentes públicas oficiales (sección 2). Esto es un estado transitorio, no el objetivo final (sección 4).

Esta declaración es deliberadamente transparente porque:

- Es lo que la Usage Policy de Anthropic espera bajo el principio de **disclosure**.
- Le da al usuario información veraz para decidir cuánto peso darle a la ficha.
- Evita la apariencia de validación clínica que el producto todavía no posee.

---

## 2. Fuentes que respaldan la curación actual

El contenido del catálogo se construye triangulando tres tipos de fuente:

### 2.1 Guías oficiales del sector salud mexicano

- **CENETEC** — Centro Nacional de Excelencia Tecnológica en Salud. Catálogo Maestro de Guías de Práctica Clínica (GPC): <https://www.cenetec-difusion.com/CMGPC/>
- **IMSS** — Guías de Práctica Clínica institucionales: <https://www.imss.gob.mx/profesionales-salud/gpc>
- **Secretaría de Salud (SSA)** — Normas Oficiales Mexicanas en salud: <https://www.gob.mx/salud/documentos/normas-oficiales-mexicanas>

### 2.2 Organismos internacionales

- **OMS / WHO** — Fichas descriptivas de enfermedades no transmisibles: <https://www.who.int/es/health-topics>
- **NIH / NIDDK** (diabetes, endocrino, renal): <https://www.niddk.nih.gov/>
- **CDC** (prevalencia, factores de riesgo): <https://www.cdc.gov/>
- **Mayo Clinic** (lenguaje accesible para `lay_explainer_es`): <https://www.mayoclinic.org/es>

### 2.3 Literatura científica

- **PubMed** para revisiones sistemáticas y consensos: <https://pubmed.ncbi.nlm.nih.gov/>
- Preferencia por revisiones publicadas en los últimos 5 años.

Cuando una fila del catálogo se modifica, en el commit que la introduce debería citarse la fuente principal usada (todavía no es estricto en el repo del catálogo — ver sección 5).

---

## 3. Proceso de curación actual

1. **Selección de condiciones**: priorizadas por prevalencia en México (datos ENSANUT cuando disponibles) y por solapamiento con el modelo nutricional de Bitlan.
2. **Redacción de `lay_explainer_es`**: lenguaje plano (objetivo: nivel lectura ~8.º grado), sin tecnicismos sin explicar, sin lenguaje absolutista.
3. **Asignación de `requires_medical_referral`**: `true` cuando la condición demanda supervisión médica activa para cualquier cambio de alimentación o estilo de vida (ej.: diabetes tipo 1). `false` cuando ajustes de estilo de vida son seguros sin acompañamiento clínico.
4. **`prevalence_mx`**: solo se rellena si hay fuente epidemiológica MX verificable (ENSANUT, IMSS, INEGI). Si no hay dato, queda `null` — preferimos vacío a inventado.
5. **Revisión cruzada**: dos personas del equipo de producto leen la ficha antes de marcarla `active=true` en la base de datos.

---

## 4. Compromiso público de incorporar revisión clínica formal

Bitlan se compromete a incorporar revisión por profesional de la salud colegiado (médico general o de especialidad afín según la categoría de la condición) **como objetivo de producto**. No hay fecha definida al cierre de este archivo (`v0.1.2`).

Cuando suceda, este archivo se actualizará para listar:

- Nombre completo del revisor.
- Cédula profesional (verificable en el Registro Nacional de Profesionistas: <https://www.cedulaprofesional.sep.gob.mx/>).
- Especialidad y rama de la medicina.
- Alcance de la revisión (¿todo el catálogo? ¿por categoría?).
- Fecha del último review por condición.
- Cadencia de re-revisión.

Hasta entonces, **toda ficha del catálogo está sujeta a esta limitación** y debe leerse como "información educativa curada por el equipo de producto de Bitlan", no como "información validada por un médico".

---

## 5. Cómo reportar errores o sugerencias

Si detectas:

- Un dato incorrecto en una ficha del catálogo.
- Una condición que debería tener `requires_medical_referral: true` y no lo tiene (o viceversa).
- Una explicación que induzca a confusión o que use lenguaje absolutista.
- Una fuente que debamos incorporar o retirar.

Escríbenos a **<legal@bitlan.mx>** con el `slug` de la condición y la observación. Las correcciones se aplican vía pull request al repo del catálogo y se reflejan en la siguiente versión de la skill (cache TTL de 1h).

---

## 6. Limitaciones conocidas

- **Sesgo de fuente**: priorizamos guías mexicanas y latinoamericanas, lo que puede limitar la aplicabilidad a otras geografías. Las fichas no incluyen rangos clínicos específicos de país.
- **Actualización no automatizada**: no hay un workflow que monitoree cambios en CENETEC o GPC del IMSS; las actualizaciones dependen de la atención del equipo.
- **Sin revisión por par-clínico**: las decisiones sobre `requires_medical_referral` no han pasado por consenso clínico formal; reflejan una lectura conservadora (en duda, marcar `true`).
- **Cobertura limitada**: ~39 condiciones al momento de `v0.1.2`, sesgadas hacia endocrino-metabólico, reproductivo y cardiometabólico (alineado al producto Bitlan).

Estas limitaciones se declaran aquí precisamente porque son las que un revisor clínico colegiado ayudaría a cerrar.

---

## 7. Versionado de este archivo

| Versión skill | Cambio en este archivo |
|---|---|
| `0.1.2` | Creación del archivo. Estado: curación por equipo de producto sobre fuentes públicas; sin revisor médico formal; compromiso público de incorporarlo. |

Para preguntas regulatorias o de cumplimiento: **<legal@bitlan.mx>**
