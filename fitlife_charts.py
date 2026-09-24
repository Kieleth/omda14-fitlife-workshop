"""Chart requests choose a calculation; all plotted values come from pandas."""

import math
import re

import pandas as pd
import streamlit as st

from fitlife_tools import PLANS, tool_schema

METRICS = {
    'member_records': ('Registros de socio y mes', 'registros', 'número de filas del periodo y grupo, incluyendo activos y bajas'),
    'distinct_members': ('Socios distintos observados', 'socios', 'member_id distintos del periodo y grupo, incluyendo activos y bajas'),
    'active_members': ('Socios activos distintos', 'socios', 'member_id distintos con status=active dentro de cada grupo y periodo'),
    'churn_rate': ('Tasa de bajas', '%', 'filas churned / todas las filas del grupo × 100; denominador de registros socio-mes'),
    'revenue_active': ('Ingresos observados de activos', '€', 'suma de price_paid en filas active del periodo, incluidos descuentos'),
    'mean_margin': ('Margen medio por registro', '€/registro', 'media de price_paid menos cost_to_serve, en todas las filas del grupo'),
}
PARAMETERS = {
    'metric': {'type': 'string', 'enum': list(METRICS)},
    'group_by': {'type': 'string', 'enum': ['month', 'plan', 'center']},
    'plan': {'type': 'string', 'enum': [*PLANS, 'all']},
    'start_month': {'type': 'string', 'description': "YYYY-MM del CSV, 'primero' o 'ultimo'."},
    'end_month': {'type': 'string', 'description': "YYYY-MM del CSV o 'ultimo'."},
    'kind': {'type': 'string', 'enum': ['bar', 'line']},
    'split_by_plan': {'type': 'boolean', 'description': 'Series por plan, solo con group_by=month y plan=all.'},
}
CHART_TOOLS = [tool_schema('crear_grafico', 'Calcula y dibuja un gráfico a partir del CSV. Nunca recibas cifras inventadas.', PARAMETERS)]


def build_chart(df, metric, group_by, plan, start_month, end_month, kind, split_by_plan):
    if not isinstance(metric, str) or metric not in METRICS:
        raise ValueError('Métrica desconocida. Consulta METRICS en fitlife_charts.py.')
    if group_by not in ('month', 'plan', 'center') or plan not in (*PLANS, 'all') or kind not in ('bar', 'line'):
        raise ValueError('Agrupación, plan o tipo de gráfico no permitido.')
    if type(split_by_plan) is not bool or (split_by_plan and (group_by != 'month' or plan != 'all')):
        raise ValueError('Separar por plan requiere group_by=month y plan=all.')
    if kind == 'line' and group_by != 'month':
        raise ValueError('Usa barras para comparar planes o centros; las líneas de este ejercicio representan meses.')
    fields = {'month', 'member_id', 'plan', 'center', 'status', 'price_paid', 'cost_to_serve'}
    if not fields <= set(df.columns):
        raise ValueError('Faltan columnas del CSV: ' + ', '.join(sorted(fields - set(df.columns))))
    if df[list(fields)].isna().any().any():
        raise ValueError('Hay datos ausentes en las columnas necesarias. Revisa el CSV antes de dibujar.')
    if df.empty or not df['month'].map(lambda v: isinstance(v, str) and re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])', v) is not None).all():
        raise ValueError('El CSV necesita filas con meses YYYY-MM válidos.')
    if not df['status'].isin(['active', 'churned']).all() or not df['plan'].isin(PLANS).all():
        raise ValueError('Hay estados o planes desconocidos en el CSV.')
    if df.duplicated(['member_id', 'month']).any():
        raise ValueError('Hay registros duplicados de socio y mes. No se dibuja para evitar contar dos veces.')
    for field in ('price_paid', 'cost_to_serve'):
        if not df[field].map(lambda v: type(v) in (int, float) and math.isfinite(v) and v >= 0).all():
            raise ValueError(f'{field} contiene importes ausentes, negativos o no finitos.')
    months = set(df['month'])
    start = df['month'].min() if start_month == 'primero' else df['month'].max() if start_month == 'ultimo' else start_month
    end = df['month'].max() if end_month == 'ultimo' else end_month
    if not isinstance(start, str) or not isinstance(end, str) or start not in months or end not in months or start > end:
        raise ValueError('El intervalo debe usar meses del CSV y tener inicio anterior o igual al final.')
    rows = df[df['month'].between(start, end)]
    if plan != 'all':
        rows = rows[rows['plan'] == plan]
    if rows.empty:
        raise ValueError('No hay datos para ese plan y periodo. No se dibujan ceros inventados.')
    grouping = [group_by] + (['plan'] if split_by_plan else [])
    if group_by == 'month':
        expected = set(pd.period_range(start, end, freq='M').astype(str))
        populations = [rows[rows['plan'] == p] for p in PLANS] if split_by_plan else [rows]
        if any(set(part['month']) != expected for part in populations):
            raise ValueError('Faltan meses en una serie. No se unen puntos a través de datos ausentes.')
    values = []
    for keys, group in rows.groupby(grouping, sort=True):
        keys = keys if isinstance(keys, tuple) else (keys,)
        active = group[group['status'] == 'active']
        if metric == 'member_records':
            value = len(group)
        elif metric == 'distinct_members':
            value = int(group['member_id'].nunique())
        elif metric == 'active_members':
            value = int(active['member_id'].nunique())
        elif metric == 'churn_rate':
            value = float((group['status'] == 'churned').sum() / len(group) * 100)
        elif metric == 'revenue_active':
            value = float(active['price_paid'].sum())
        elif metric == 'mean_margin':
            value = float((group['price_paid'] - group['cost_to_serve']).mean())
        else:
            raise ValueError('La métrica está anunciada en METRICS pero falta implementar su cálculo.')
        values.append({**dict(zip(grouping, keys)), 'value': value, 'registros': len(group)})
    title, unit, definition = METRICS[metric]
    return {'kind': kind, 'x': group_by, 'series': 'plan' if split_by_plan else None,
            'metric': metric, 'title': title, 'unit': unit, 'definition': definition,
            'filters': {'plan': plan, 'start_month': start, 'end_month': end}, 'data': values}


def execute_chart(df, name, arguments):
    if name != 'crear_grafico' or not isinstance(arguments, dict) or set(arguments) != set(PARAMETERS):
        raise ValueError('crear_grafico necesita exactamente los argumentos de su definición. No acepta código ni valores a dibujar.')
    return build_chart(df, **arguments)


def draw_chart(chart, key):
    """Render only the small declarative format generated above, including restored turns."""
    required = {'kind', 'x', 'series', 'metric', 'title', 'unit', 'definition', 'filters', 'data'}
    if not isinstance(chart, dict) or set(chart) != required:
        raise ValueError('El gráfico guardado no tiene el formato de este ejercicio.')
    if chart['kind'] not in ('bar', 'line') or chart['x'] not in ('month', 'plan', 'center') or chart['series'] not in (None, 'plan'):
        raise ValueError('El gráfico guardado contiene un tipo o eje desconocido.')
    if (not isinstance(chart['data'], list) or not chart['data'] or len(chart['data']) > 1000
            or chart['metric'] not in METRICS or not isinstance(chart['filters'], dict)
            or set(chart['filters']) != {'plan', 'start_month', 'end_month'}):
        raise ValueError('El gráfico guardado necesita datos, métrica y filtros válidos.')
    for row in chart['data']:
        fields = {chart['x'], 'value', 'registros'} | ({'plan'} if chart['series'] else set())
        if (not isinstance(row, dict) or set(row) != fields
                or type(row['value']) not in (int, float) or not math.isfinite(row['value'])
                or type(row['registros']) is not int or row['registros'] <= 0):
            raise ValueError('El gráfico guardado contiene una fila incompleta o un valor no finito.')
    frame = pd.DataFrame(chart['data'])
    filters = chart['filters']
    st.subheader(chart['title'])
    st.caption(f"{filters['start_month']} a {filters['end_month']} · plan: {filters['plan']} · {chart['definition']}")
    options = dict(x=chart['x'], y='value', color=chart['series'],
                   x_label={'month': 'Mes', 'plan': 'Plan', 'center': 'Centro'}[chart['x']], y_label=chart['unit'])
    if chart['kind'] == 'line':
        st.line_chart(frame, **options)
    else:
        st.bar_chart(frame, **options, stack=False)
    with st.expander('Tabla exacta detrás del gráfico'):
        st.dataframe(frame, hide_index=True)
        st.download_button('Guardar datos del gráfico', frame.to_csv(index=False), 'fitlife-grafico.csv', 'text/csv',
                           key=key, on_click='ignore')


SYSTEM = '''Eres el analista visual de FitLife. Solo crear_grafico calcula los datos y dibuja.
Usa esa herramienta cuando te pidan un gráfico. No inventes valores ni escribas código.
Si falta una métrica o es ambigua, pregunta antes de llamar. Indica los filtros que vas a usar.
Si no se indica periodo, usa start_month=ultimo y end_month=ultimo y dilo explícitamente.
Si se pide evolución sin periodo, usa primero a ultimo. Si no se indica plan, usa all y dilo.
Usa line para evolución temporal y bar para comparar categorías. Para evolución por plan, group_by=month,
plan=all y split_by_plan=true. Usa el historial para resolver seguimientos como "ahora en barras".
No confundas churn con número de bajas: churn_rate es porcentaje de registros socio-mes.
member_records cuenta filas; distinct_members cuenta personas observadas incluyendo bajas; active_members solo activos.
Las herramientas no calculan causalidad, predicciones ni LTV completo. Si no pueden responder, explica qué falta.'''
