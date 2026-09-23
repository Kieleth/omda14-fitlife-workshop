"""Session 4: explicit calculations over the existing public FitLife course dataset.

This module performs no network calls when imported. API calls happen only when
an app user submits a question. The provider and dataset are unchanged from
exercises/paso_15.py in public Kieleth/omda14-fitlife-workshop, clase/sesion-3.
Tool results contain aggregate counts and amounts, never member-level rows.
"""

from copy import deepcopy
import json
import math
from time import perf_counter

from chat_history import api_messages

PLANS = ('basic', 'premium', 'family')


def select_month(df, plan, month):
    required = {'member_id', 'month', 'plan', 'status', 'price_paid', 'cost_to_serve'}
    if not required <= set(df.columns):
        raise ValueError('Faltan columnas de FitLife: ' + ', '.join(sorted(required - set(df.columns))))
    if df[list(required)].isna().any().any():
        raise ValueError('Hay datos ausentes en las columnas necesarias. Revisa el dataset antes de calcular.')
    if not df['status'].isin(['active', 'churned']).all():
        raise ValueError('Estado desconocido. Usa active o churned; no se puede calcular el denominador.')
    for field in ('price_paid', 'cost_to_serve'):
        if not df[field].map(lambda value: type(value) in (int, float) and math.isfinite(value) and value >= 0).all():
            raise ValueError(f'{field} necesita importes finitos mayores o iguales que cero.')
    if not isinstance(plan, str) or plan not in PLANS:
        raise ValueError('Plan desconocido. Usa basic, premium o family.')
    if not isinstance(month, str) or month not in {*df['month'].unique(), 'ultimo'}:
        raise ValueError("Mes desconocido. Usa YYYY-MM presente en los datos o 'ultimo'.")
    selected = df['month'].max() if month == 'ultimo' else month
    rows = df[(df['plan'] == plan) & (df['month'] == selected)]
    if rows.empty:
        raise ValueError(f'No hay registros para {plan} en {selected}.')
    if rows['member_id'].duplicated().any():
        raise ValueError('Hay socios duplicados en el mes. Revisa el dataset antes de calcular.')
    return selected, rows


def resumen_plan(df, plan, month):
    selected, rows = select_month(df, plan, month)
    lost = int((rows['status'] == 'churned').sum())
    return {
        'plan': plan, 'mes': selected, 'registros_socio_mes': len(rows),
        'socios_activos': int((rows['status'] == 'active').sum()), 'bajas': lost,
        'churn_porcentaje': lost / len(rows) * 100,
        'denominador_churn': 'todos los registros del plan en ese mes, activos y bajas',
        'precio_medio_pagado_euros': float(rows['price_paid'].mean()),
        'margen_medio_euros': float((rows['price_paid'] - rows['cost_to_serve']).mean()),
    }


def escenario_precio(df, plan, month, new_price):
    if type(new_price) not in (int, float) or not math.isfinite(new_price) or new_price < 0:
        raise ValueError('new_price debe ser un número finito mayor o igual que cero.')
    selected, rows = select_month(df, plan, month)
    active = rows[rows['status'] == 'active']
    current = float(active['price_paid'].sum())
    simulated = len(active) * new_price
    return {
        'plan': plan, 'mes': selected, 'socios_activos': len(active),
        'nuevo_precio_euros': new_price, 'ingreso_observado_euros': current,
        'ingreso_simulado_euros': simulated, 'cambio_ingreso_euros': simulated - current,
        'supuesto': 'los mismos socios activos pagan todos el precio nuevo, sin descuentos adicionales',
        'no_calculado': 'cambios de bajas, captación, costes o competidores; no es una predicción',
    }


def tool_schema(name, description, properties):
    return {'type': 'function', 'function': {
        'name': name, 'description': description, 'strict': True,
        'parameters': {'type': 'object', 'properties': properties,
                       'required': list(properties), 'additionalProperties': False},
    }}


PARAMETERS = {
    'plan': {'type': 'string', 'enum': list(PLANS)},
    'month': {'type': 'string', 'description': "Mes YYYY-MM o 'ultimo' para el último mes del dataset."},
}
TOOLS = [
    tool_schema('resumen_plan', 'Calcula socios, bajas, churn y margen de un plan en un mes.', PARAMETERS),
    tool_schema('escenario_precio', 'Escenario de ingresos a población fija. No predice retención ni captación.',
                {**PARAMETERS, 'new_price': {'type': 'number', 'description': 'Precio uniforme simulado en euros.'}}),
]


def execute_tool(df, name, arguments):
    allowed = {'resumen_plan': (resumen_plan, {'plan', 'month'}),
               'escenario_precio': (escenario_precio, {'plan', 'month', 'new_price'})}
    if name not in allowed:
        raise ValueError(f'Herramienta no permitida: {name}.')
    function, fields = allowed[name]
    if not isinstance(arguments, dict) or set(arguments) != fields:
        raise ValueError(f'{name} necesita exactamente estos argumentos: {", ".join(sorted(fields))}.')
    return function(df, **arguments)


SYSTEM = '''Eres el analista de FitLife. Usa las herramientas para calcular cifras.
Si falta el mes, usa ultimo: significa el último mes de los datos, no el mes actual.
Si falta el plan y el historial no lo aclara, pide que lo especifiquen.
En cada cifra indica periodo, población y unidad. No inventes respuestas que las
herramientas no pueden calcular. Un escenario a población fija no predice el efecto
de bajar precios. Distingue dato, supuesto y recomendación. Asociación no es causalidad.'''


def ask_with_tools(client, df, history, model, tools):
    messages = api_messages(SYSTEM, history)
    trace = []
    started = perf_counter()
    for round_number in range(4):
        options = {'model': model, 'messages': deepcopy(messages)}
        if round_number < 3:
            options.update(tools=tools, parallel_tool_calls=False)
        response = client.chat.completions.create(**options)
        message = response.choices[0].message
        if response.usage is None:
            raise ValueError('La API no devolvió el uso de tokens. No podemos registrar la petición.')
        entry = {'request': deepcopy(options), 'response': message.model_dump(exclude_none=True),
                 'usage': response.usage.model_dump(), 'tool_results': []}
        trace.append(entry)
        if not message.tool_calls:
            if not message.content:
                raise ValueError('La API terminó sin texto ni petición de herramienta. Revisa la respuesta.')
            return {'role': 'assistant', 'content': message.content,
                    'details': {'model': model, 'seconds': perf_counter() - started, 'calls': trace}}
        if round_number == 3 or len(message.tool_calls) != 1:
            raise ValueError('Se esperaba una herramienta por ronda y una respuesta final tras tres rondas.')
        call = message.tool_calls[0]
        names = {tool['function']['name'] for tool in tools}
        if call.type != 'function' or call.function.name not in names:
            raise ValueError('El modelo pidió una herramienta que esta app no ha ofrecido.')
        try:
            arguments = json.loads(call.function.arguments)
        except (ValueError, TypeError) as exc:
            raise ValueError('Los argumentos de la herramienta no son JSON válido.') from exc
        result = execute_tool(df, call.function.name, arguments)
        messages.append({'role': 'assistant', 'content': message.content,
                         'tool_calls': [call.model_dump()]})
        messages.append({'role': 'tool', 'tool_call_id': call.id,
                         'content': json.dumps(result, ensure_ascii=False, allow_nan=False)})
        entry['tool_results'].append({'name': call.function.name, 'arguments': arguments, 'result': result})
    raise AssertionError('El bucle debe devolver una respuesta o explicar el fallo.')
