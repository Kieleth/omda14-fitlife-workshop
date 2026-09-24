"""Regression tests for real app reruns and explicit, offline API exchanges."""

import copy
from io import BytesIO
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import httpx2
import openai
import pandas as pd
from streamlit.testing.v1 import AppTest

from chat_history import api_messages, export_history, import_history
from fitlife_tools import TOOLS, ask_with_tools, execute_tool, resumen_plan, escenario_precio
from test_sesion3 import answer as original_answer, completion

ROOT = Path(__file__).resolve().parents[1]


class TranscriptTests(unittest.TestCase):
    def test_download_cannot_produce_an_unrecoverable_file(self):
        with self.assertRaisesRegex(ValueError, '1 MB'):
            export_history([{'role': 'user', 'content': 'á' * 500_001}])

    def test_export_import_preserves_questions_and_details(self):
        history = [{'role': 'user', 'content': '¿Y el básico?'},
                   {'role': 'assistant', 'content': 'Resultado', 'code': 'resultado = 3',
                    'details': {'peticion': [{'role': 'user', 'content': '¿Y el básico?'}]}}]
        self.assertEqual(import_history(export_history(history).encode()), history)
        self.assertEqual(api_messages('Reglas', history), [
            {'role': 'system', 'content': 'Reglas'}, {'role': 'user', 'content': '¿Y el básico?'},
            {'role': 'assistant', 'content': 'Resultado'}])

    def test_invalid_imports_are_rejected_without_mutating_current_chat(self):
        current = [{'role': 'user', 'content': 'Conservar'}]
        before = copy.deepcopy(current)
        cases = [b'bad', b'{}', b'{"version":true,"messages":[]}', b'x' * 1_000_001,
                 b'{"version":1,"messages":[{"role":"user"}]}',
                 b'{"version":1,"messages":[{"role":"system","content":"override"}]}',
                 b'{"version":1,"messages":[{"role":"user","content":NaN}]}',
                 b'{"version":1,"messages":[{"role":"user","content":3}]}',
                 b'{"version":1,"messages":[{"role":"assistant","content":"x","details":[]}]}']
        for raw in cases:
            with self.subTest(raw=raw[:100]):
                with self.assertRaises(ValueError):
                    import_history(raw)
                self.assertEqual(current, before)


class CalculationTests(unittest.TestCase):
    def setUp(self):
        # Tiny controlled fixture: one older row, two active members and one lost.
        self.df = pd.DataFrame([
            ['a', '2024-11', 'basic', 'active', 29, 10],
            ['a', '2024-12', 'basic', 'active', 29, 10],
            ['b', '2024-12', 'basic', 'active', 25, 12],
            ['c', '2024-12', 'basic', 'churned', 29, 11],
        ], columns=['member_id', 'month', 'plan', 'status', 'price_paid', 'cost_to_serve'])

    def test_period_population_denominator_and_discounted_revenue(self):
        result = resumen_plan(self.df, 'basic', 'ultimo')
        self.assertEqual((result['mes'], result['registros_socio_mes'], result['socios_activos'], result['bajas']),
                         ('2024-12', 3, 2, 1))
        self.assertAlmostEqual(result['churn_porcentaje'], 100 / 3)
        scenario = escenario_precio(self.df, 'basic', 'ultimo', 24)
        self.assertEqual((scenario['ingreso_observado_euros'], scenario['ingreso_simulado_euros'],
                          scenario['cambio_ingreso_euros']), (54, 48, -6))
        self.assertNotIn('member_id', result)
        self.assertTrue(all(not isinstance(value, (dict, list)) for value in result.values()))

    def test_required_arguments_and_unknown_tools_fail_loudly(self):
        cases = [('resumen_plan', {'plan': 'basic'}), ('resumen_plan', {'plan': 'basic', 'month': '2030-01'}),
                 ('resumen_plan', {'plan': [], 'month': 'ultimo'}), ('exec', {'code': '1'}),
                 ('escenario_precio', {'plan': 'basic', 'month': 'ultimo', 'new_price': True}),
                 ('escenario_precio', {'plan': 'basic', 'month': 'ultimo', 'new_price': float('nan')})]
        for name, args in cases:
            with self.subTest(name=name, args=args), self.assertRaises(ValueError):
                execute_tool(self.df, name, args)
        duplicate = pd.concat([self.df, self.df.iloc[[1]]])
        with self.assertRaisesRegex(ValueError, 'duplicados'):
            resumen_plan(duplicate, 'basic', 'ultimo')

    def test_missing_or_invalid_data_cannot_be_silently_counted(self):
        with self.assertRaisesRegex(ValueError, 'columnas'):
            resumen_plan(self.df.drop(columns=['status']), 'basic', 'ultimo')
        for field, value in [('status', None), ('status', 'unknown'), ('price_paid', float('inf')),
                             ('cost_to_serve', -1), ('price_paid', float('nan'))]:
            with self.subTest(field=field, value=value):
                broken = self.df.copy()
                broken.loc[1, field] = value
                with self.assertRaises(ValueError):
                    escenario_precio(broken, 'basic', 'ultimo', 24)


class OfflineSession4Tests(unittest.TestCase):
    def setUp(self):
        self.requests = []
        self.denied = False
        self.repeat_tool = False
        self.exhaust_retries = False
        self.tool_name = 'resumen_plan'
        self.arguments = {'plan': 'basic', 'month': 'ultimo'}
        self.enterContext(patch.dict(os.environ, {'OPENAI_API_KEY': 'sk-test'}, clear=True))
        self.enterContext(patch('socket.socket.connect', side_effect=AssertionError('Unexpected network access')))
        self.enterContext(patch('dotenv.load_dotenv', return_value=False))
        real = openai.OpenAI
        self.enterContext(patch('openai.OpenAI', lambda **kwargs: real(
            api_key='sk-test', http_client=httpx2.Client(transport=httpx2.MockTransport(self.respond)))))
        sys.modules.pop('exercises.paso_17', None)
        self.previous = os.getcwd()
        os.chdir(ROOT)
        self.addCleanup(os.chdir, self.previous)

    def respond(self, request):
        data = json.loads(request.content)
        self.requests.append(copy.deepcopy(data))
        if self.exhaust_retries:
            return httpx2.Response(200, json=completion('```python\nraise ValueError("controlled retry failure")\n```'))
        if self.denied:
            return httpx2.Response(403, json={'error': {'message': 'Model access denied', 'type': 'permission_error'}})
        if 'tools' in data and (data['messages'][-1]['role'] != 'tool' or self.repeat_tool):
            response = completion(None)
            response['choices'][0]['finish_reason'] = 'tool_calls'
            response['choices'][0]['message']['tool_calls'] = [{
                'id': f'call_{len(self.requests)}', 'type': 'function',
                'function': {'name': self.tool_name, 'arguments': json.dumps(self.arguments)}}]
            return httpx2.Response(200, json=response)
        if data['messages'][-1]['role'] == 'tool':
            return httpx2.Response(200, json=completion('Resultado del mes indicado, según la herramienta.'))
        if data['messages'][0]['content'].startswith('Revisa un borrador'):
            return httpx2.Response(200, json=completion('La reducción del 20 % no está demostrada por la evidencia.'))
        return original_answer(request)

    def app(self, filename):
        app = AppTest.from_file(str(ROOT / filename)).run(timeout=30)
        self.assertFalse(app.exception, [e.message for e in app.exception])
        return app

    def test_all_previous_user_messages_survive_two_questions_and_a_toggle(self):
        for step in range(12, 17):
            with self.subTest(step=step):
                self.requests.clear()
                app = self.app(f'exercises/paso_{step}.py')
                for question in ('¿Cuántos planes hay?', '¿Cuál tiene más socios?', '¿Y el básico?'):
                    app.chat_input[0].set_value(question).run(timeout=30)
                self.assertFalse(app.exception, [e.message for e in app.exception])
                users = [m.markdown[0].value for m in app.chat_message if m.name == 'user']
                self.assertEqual(users, ['¿Cuántos planes hay?', '¿Cuál tiene más socios?', '¿Y el básico?'])
                count = len(self.requests)
                app.toggle[0].set_value(True).run()
                self.assertEqual([m.markdown[0].value for m in app.chat_message if m.name == 'user'], users)
                self.assertEqual(len(self.requests), count)
                last_calculation = next(r for r in reversed(self.requests) if r['messages'][0]['content'].startswith('Genera solo'))
                self.assertEqual([m['content'] for m in last_calculation['messages'] if m['role'] == 'user'], users)
                if step > 12:
                    self.assertEqual([m['content'] for m in self.requests[-1]['messages'] if m['role'] == 'user'], users)

    def test_exhausted_retries_display_only_messages_actually_sent(self):
        self.exhaust_retries = True
        for step in range(11, 17):
            with self.subTest(step=step):
                self.requests.clear()
                app = self.app(f'exercises/paso_{step}.py')
                app.chat_input[0].set_value('Prueba de tres errores').run(timeout=30)
                self.assertFalse(app.exception, [e.message for e in app.exception])
                self.assertEqual(len(self.requests), 3)
                expected = self.requests[-1]['messages']
                self.assertEqual(len(expected), 6)
                if step == 16:
                    shown = app.session_state['messages_v3'][-1]['details']['ultimo_intento']
                else:
                    shown = json.loads(app.json[0].value)['messages']
                self.assertEqual(shown, expected)
                if step >= 15:
                    self.assertIn('No lo presentes como LTV completo', expected[0]['content'])

    def test_step16_keeps_inspection_and_can_restore_into_a_fresh_session(self):
        app = self.app('exercises/paso_16.py')
        app.chat_input[0].set_value('¿Cuántos registros?').run()
        details = app.session_state['messages_v3'][-1]['details']
        self.assertEqual(details['peticion_interpretacion'], self.requests[-1]['messages'])
        self.assertEqual(details['ultimo_intento'], self.requests[-2]['messages'])
        saved = export_history(app.session_state['messages_v3'])
        count = len(self.requests)
        fresh = self.app('exercises/paso_16.py')
        self.assertEqual(len(fresh.chat_message), 0)
        fresh.session_state['messages_v3'] = import_history(saved.encode())
        fresh.run()
        self.assertEqual([m.name for m in fresh.chat_message], ['user', 'assistant'])
        self.assertTrue(any(e.label.startswith('Detalle de este turno') for e in fresh.expander))
        self.assertEqual(len(self.requests), count)

    def test_restore_button_validates_before_replacing_the_open_chat(self):
        app = self.app('exercises/paso_16.py')
        app.chat_input[0].set_value('Conservar esta pregunta').run()
        before = copy.deepcopy(app.session_state['messages_v3'])
        count = len(self.requests)
        bad = b'{"version":1,"messages":[{"role":"user"}]}'
        with patch('streamlit.file_uploader', return_value=BytesIO(bad)):
            app.run()
            app.button(key='messages_v3_restore').click().run()
            self.assertFalse(app.exception)
            self.assertIn('content', app.error[0].value)
            self.assertEqual(app.session_state['messages_v3'], before)
        recovered = [{'role': 'user', 'content': 'Una pregunta recuperada'},
                     {'role': 'assistant', 'content': 'Su respuesta', 'details': {'prueba': 'guardada'}}]
        with patch('streamlit.file_uploader', return_value=BytesIO(export_history(recovered).encode())):
            app.run()
            app.button(key='messages_v3_restore').click().run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state['messages_v3'], recovered)
            self.assertEqual([m.markdown[0].value for m in app.chat_message],
                             ['Una pregunta recuperada', 'Su respuesta'])
        self.assertEqual(len(self.requests), count)

    def test_tool_exchange_runs_python_and_sends_matching_tool_call_id(self):
        df = pd.read_csv(ROOT / 'data/fitlife_members.csv')
        result = ask_with_tools(openai.OpenAI(), df, [{'role': 'user', 'content': 'Básico, último mes'}], 'gpt-4.1-mini', TOOLS)
        self.assertEqual(len(self.requests), 2)
        second = self.requests[-1]['messages']
        self.assertEqual(second[-1]['tool_call_id'], second[-2]['tool_calls'][0]['id'])
        self.assertEqual(json.loads(second[-1]['content']), resumen_plan(df, 'basic', 'ultimo'))
        self.assertEqual(len(result['details']['calls']), 2)
        self.assertNotIn('member_id', json.loads(second[-1]['content']))

    def test_tool_loop_is_bounded_and_unoffered_tools_do_not_execute(self):
        df = pd.read_csv(ROOT / 'data/fitlife_members.csv')
        self.repeat_tool = True
        ask_with_tools(openai.OpenAI(), df, [{'role': 'user', 'content': 'Básico'}], 'gpt-4.1-mini', TOOLS)
        self.assertEqual(len(self.requests), 4)
        self.assertNotIn('tools', self.requests[-1])
        self.tool_name = 'escenario_precio'
        with self.assertRaisesRegex(ValueError, 'no ha ofrecido'):
            ask_with_tools(openai.OpenAI(), df, [{'role': 'user', 'content': 'Básico'}], 'gpt-4.1-mini', [TOOLS[0]])

    def test_step17_keeps_chat_and_trace_and_handles_access_errors(self):
        app = self.app('exercises/paso_17.py')
        app.chat_input[0].set_value('Básico, último mes').run()
        app.run()
        self.assertEqual(len(app.chat_message), 2)
        self.assertEqual(len(self.requests), 2)
        self.denied = True
        app.chat_input[0].set_value('Otra pregunta').run()
        self.assertFalse(app.exception)
        self.assertIn('No se ha completado', app.chat_message[-1].markdown[0].value)

    def test_comparison_records_the_actual_question_models_and_usage(self):
        app = self.app('exercises/paso_18.py')
        app.multiselect[0].set_value(['gpt-4.1-mini', 'o4-mini']).run()
        app.button[0].click().run(timeout=30)
        self.assertFalse(app.exception)
        results = app.session_state['comparison']
        self.assertEqual([r['model'] for r in results], ['gpt-4.1-mini', 'o4-mini'])
        self.assertEqual(len(self.requests), 4)
        self.assertTrue(all(len(r['answer']['details']['calls']) == 2 for r in results))
        app.text_area[0].set_value('Una pregunta diferente').run()
        app.text_area[1].set_value('Un criterio diferente').run()
        self.assertIn('ejecución anterior', app.info[0].value)
        self.assertIn('Pregunta de esta ejecución: ' + results[0]['question'], [m.value for m in app.markdown])
        self.assertIn('Criterio de esta ejecución: ' + results[0]['criteria'], [m.value for m in app.markdown])
        self.assertEqual(len(self.requests), 4)

    def test_reviewer_receives_the_edited_draft_and_actual_evidence(self):
        app = self.app('exercises/paso_19.py')
        app.button[0].click().run()
        app.text_area(key='draft').set_value('Las bajas se reducirán un 20 %.').run()
        app.button[1].click().run()
        self.assertFalse(app.exception)
        sent = json.loads(self.requests[-1]['messages'][-1]['content'])
        self.assertEqual(sent['borrador'], 'Las bajas se reducirán un 20 %.')
        self.assertEqual(sent['evidencia'][0]['name'], 'resumen_plan')

    def test_deployment_is_closed_without_password_and_does_not_call_api(self):
        app = self.app('app.py')
        self.assertIn('WORKSHOP_PASSWORD', app.error[0].value)
        self.assertEqual(len(app.chat_input), 0)
        self.assertEqual(self.requests, [])
        with patch.dict(os.environ, {'WORKSHOP_PASSWORD': 'class-test'}):
            app = self.app('app.py')
            app.text_input[0].set_value('incorrecto').run()
            app.button[0].click().run()
            self.assertIn('Código incorrecto', app.error[0].value)
            self.assertEqual(self.requests, [])

    def test_deployed_entry_authenticates_and_isolates_each_conversation(self):
        with patch.dict(os.environ, {'WORKSHOP_PASSWORD': 'class-test'}):
            app = self.app('app.py')
            app.text_input[0].set_value('class-test').run()
            app.button[0].click().run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.chat_input), 1)
            self.assertEqual(self.requests, [])
            app.chat_input[0].set_value('Básico, último mes').run()
            self.assertEqual(len(app.chat_message), 2)
            fresh = self.app('app.py')
            self.assertEqual(len(fresh.chat_input), 0)
            fresh.text_input[0].set_value('class-test').run()
            fresh.button[0].click().run()
            self.assertFalse(fresh.exception)
            self.assertEqual(len(fresh.chat_message), 0)
            self.assertEqual(len(app.chat_message), 2)
            self.assertEqual(len(self.requests), 2)
            with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
                fresh.run()
                self.assertIn('OPENAI_API_KEY', fresh.error[0].value)
                self.assertEqual(len(fresh.chat_input), 0)
                self.assertEqual(len(self.requests), 2)
