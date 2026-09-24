# Preguntas de test: FitLife

Estas preguntas las usaremos durante las sesiones para evaluar cómo responde el sistema.
Las mismas preguntas se repiten en cada sesión para ver la mejora.

---

| # | Pregunta | Dificultad |
|---|----------|-----------|
| 1 | ¿Cuántos socios activos hay en el último mes? | Fácil |
| 2 | ¿Cuál es la distribución de socios por plan? | Fácil |
| 3 | ¿Cuál es el precio medio pagado por los socios? | Fácil |
| 4 | ¿Cuál es el margen medio por socio (price_paid menos cost_to_serve) por plan? | Media |
| 5 | ¿Cuál es la tasa de churn mensual de cada plan? | Media |
| 6 | ¿Los socios que usan la app tienen menos churn que los que no? | Media |
| 7 | ¿Qué canal de captación trae socios más fieles (menor churn)? | Media-alta |
| 8 | ¿Los socios que se dan de baja son más o menos rentables que los que se quedan? | Alta |
| 9 | ¿Las bajas del plan básico aumentaron cuando el competidor bajó precios? | Alta |
| 10 | ¿Las campañas de enero traen socios de peor calidad (más churn)? | Alta |
| 11 | ¿Cuál es el lifetime value medio por plan? | Alta |
| 12 | ¿Debería FitLife bajar el precio del plan básico? | Prescriptiva |

---

## Cómo usarlas

Antes de puntuar, fija el periodo, la población y la unidad. «Último mes» significa el último mes del dataset, no el mes del calendario actual. Una fila es un registro de socio y mes; no siempre equivale a un socio distinto.

Para la pregunta 11, distingue el ingreso observado por socio dentro de 2022-2024 del valor completo durante su vida como cliente (LTV). Sumar `price_paid` en la muestra no calcula por sí solo ese valor completo. Una respuesta válida debe declarar qué aproxima, cómo trata a quienes siguen activos y qué definición de valor usa. Reconocer que faltan datos puede ser la respuesta correcta.

En las preguntas 6, 9, 10 y 12, una diferencia entre grupos o periodos no demuestra una causa. La respuesta debe separar el cálculo observado, sus límites y cualquier supuesto usado para recomendar.

1. Haz cada pregunta al chat del sistema
2. Apunta la respuesta
3. Evalúa: ¿es correcta? ¿es inventada? ¿es parcial?
4. En sesiones posteriores, repite las mismas preguntas y compara
