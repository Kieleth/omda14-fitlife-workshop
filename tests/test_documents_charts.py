"""Offline student interactions: no credentials, external services or generated numbers."""

import copy
from io import BytesIO
import json
import os
import sys
from pathlib import Path
import unittest
from unittest.mock import patch

import httpx2
import openai
import pandas as pd
from streamlit.testing.v1 import AppTest

from chat_history import export_history, import_history
from fitlife_documents import document_chunks, load_course_documents, retrieve, select_context, answer_documents
from fitlife_charts import build_chart, execute_chart, METRICS
from test_sesion3 import completion

ROOT = Path(__file__).resolve().parents[1]


class DocumentTests(unittest.TestCase):
    def test_load_retrieve_and_changed_document_identity(self):
        chunks = load_course_documents(ROOT / 'data/conocimiento')
        self.assertEqual(len({c['file'] for c in chunks}), 3)
        selected = retrieve('plazo baja renovación', chunks, 3)
        self.assertIn('7 días naturales', selected[0]['text'])
        self.assertTrue(all(c['score'] == len(c['matched_words']) for c in selected))
        self.assertEqual(retrieve('xyzxyz', chunks, 3), [])
        before = document_chunks('prueba.md', '# Regla\n\nSiete días.'.encode())
        after = document_chunks('prueba.md', '# Regla\n\nNueve días.'.encode())
        self.assertNotEqual(before[0]['id'], after[0]['id'])
        self.assertEqual(select_context('baja', chunks, 'Sin documentos', 3), [])
        self.assertEqual(select_context('baja', chunks, 'Todos los fragmentos', 3), chunks)

    def test_unreadable_missing_and_oversized_inputs_fail_loudly(self):
        for name, raw in [('x.pdf', b'%PDF'), ('x.md', b'\xff'), ('x.md', b''), ('x.txt', b'\x00'),
                          ('x.md', b'# Solo titulo'), ('x.md', b'x' * 200_001)]:
            with self.subTest(name=name, raw=raw[:30]), self.assertRaises(ValueError):
                document_chunks(name, raw)
        with self.assertRaisesRegex(ValueError, '60.000'):
            select_context('algo', document_chunks('grande.md', b'x' * 70_000), 'Todos los fragmentos', 3)
        with self.assertRaises(ValueError):
            retrieve('baja', [], True)


class ChartCalculationTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame([
            ['a', '2024-11', 'basic', 'northside', 'active', 29., 10.],
            ['a', '2024-12', 'basic', 'northside', 'active', 29., 10.],
            ['b', '2024-12', 'basic', 'northside', 'active', 25., 12.],
            ['c', '2024-12', 'basic', 'northside', 'churned', 29., 11.],
        ], columns=['member_id', 'month', 'plan', 'center', 'status', 'price_paid', 'cost_to_serve'])
        self.args = dict(metric='churn_rate', group_by='month', plan='basic', start_month='2024-11',
                         end_month='2024-12', kind='line', split_by_plan=False)

    def test_points_match_controlled_counts_denominators_and_discounts(self):
        chart = build_chart(self.df, **self.args)
        self.assertEqual(chart['data'][0], {'month': '2024-11', 'value': 0.0, 'registros': 1})
        self.assertAlmostEqual(chart['data'][1]['value'], 100 / 3)
        revenue = build_chart(self.df, **{**self.args, 'metric': 'revenue_active'})
        self.assertEqual([r['value'] for r in revenue['data']], [29, 54])
        active = build_chart(self.df, **{**self.args, 'metric': 'active_members', 'group_by': 'plan', 'kind': 'bar'})
        self.assertEqual(active['data'][0]['value'], 2)  # 'a' occurs in two months, counts once.
        for metric, expected in [('member_records', 4), ('distinct_members', 3)]:
            chart = build_chart(self.df, **{**self.args, 'metric': metric, 'group_by': 'plan', 'kind': 'bar'})
            self.assertEqual(chart['data'][0]['value'], expected)

    def test_actual_csv_has_monthly_plan_series_and_known_last_month(self):
        actual = pd.read_csv(ROOT / 'data/fitlife_members.csv')
        chart = build_chart(actual, **{**self.args, 'plan': 'all', 'start_month': '2024-01', 'split_by_plan': True})
        self.assertEqual(len(chart['data']), 36)
        last = next(r for r in chart['data'] if r['month'] == '2024-12' and r['plan'] == 'basic')
        self.assertEqual(last['registros'], 87)
        self.assertAlmostEqual(last['value'], 8 / 87 * 100)

    def test_invalid_requests_and_missing_data_are_not_plotted_as_zero(self):
        for changed in ({'metric': 'invented'}, {'start_month': '2030-01'}, {'group_by': 'plan'},
                        {'split_by_plan': True}, {'end_month': '2024-11', 'start_month': '2024-12'}):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                build_chart(self.df, **{**self.args, **changed})
        for broken in (self.df.drop(columns=['status']), pd.concat([self.df, self.df.iloc[[0]]]),
                       self.df.assign(price_paid=float('nan'))):
            with self.assertRaises(ValueError):
                build_chart(broken, **self.args)
        missing_month = self.df.copy()
        missing_month.loc[missing_month['month'] == '2024-11', 'month'] = '2024-10'
        with self.assertRaisesRegex(ValueError, 'Faltan meses'):
            build_chart(missing_month, **{**self.args, 'start_month': '2024-10'})
        with self.assertRaises(ValueError):
            execute_chart(self.df, 'crear_grafico', {**self.args, 'values': [999]})
        with patch.dict(METRICS, {'new_metric': ('New', 'x', 'Definition')}):
            with self.assertRaisesRegex(ValueError, 'falta implementar'):
                build_chart(self.df, **{**self.args, 'metric': 'new_metric'})


class OfflineDocumentChartApps(unittest.TestCase):
    def setUp(self):
        self.requests = []
        self.bad_citation = False
        self.denied = False
        self.chart_args = dict(metric='churn_rate', group_by='month', plan='all', start_month='2024-01',
                               end_month='2024-12', kind='line', split_by_plan=True)
        self.enterContext(patch.dict(os.environ, {'OPENAI_API_KEY': 'sk-test'}, clear=True))
        self.enterContext(patch('socket.socket.connect', side_effect=AssertionError('Unexpected network')))
        self.enterContext(patch('dotenv.load_dotenv', return_value=False))
        real = openai.OpenAI
        self.enterContext(patch('openai.OpenAI', lambda **kwargs: real(
            api_key='sk-test', http_client=httpx2.Client(transport=httpx2.MockTransport(self.respond)))))
        for name in ('exercises.paso_17', 'exercises.paso_20', 'exercises.paso_21'):
            sys.modules.pop(name, None)
        previous = os.getcwd()
        os.chdir(ROOT)
        self.addCleanup(os.chdir, previous)

    def respond(self, request):
        sent = json.loads(request.content)
        self.requests.append(copy.deepcopy(sent))
        if self.denied:
            return httpx2.Response(403, json={'error': {'message': 'Denied', 'type': 'permission_error'}})
        if 'response_format' in sent:
            chunks = json.loads(sent['messages'][-1]['content'])['fragmentos']
            selected = next((c for c in chunks if '7 días naturales' in c['text']), None)
            answer = {'answer': 'La fuente establece 7 días.' if selected else 'Falta una fuente sobre el plazo.',
                      'status': 'supported' if selected else 'insufficient',
                      'source_ids': [selected['id']] if selected else []}
            if self.bad_citation:
                answer['source_ids'] = ['invented:1']
            return httpx2.Response(200, json=completion(json.dumps(answer)))
        if sent['messages'][-1]['role'] == 'tool':
            return httpx2.Response(200, json=completion('Gráfico calculado sobre registros del periodo solicitado.'))
        response = completion(None)
        response['choices'][0]['finish_reason'] = 'tool_calls'
        response['choices'][0]['message']['tool_calls'] = [{
            'id': f'call_{len(self.requests)}', 'type': 'function',
            'function': {'name': 'crear_grafico', 'arguments': json.dumps(self.chart_args)}}]
        return httpx2.Response(200, json=response)

    def app(self, step):
        app = AppTest.from_file(str(ROOT / f'exercises/paso_{step}.py')).run(timeout=30)
        self.assertFalse(app.exception, [e.message for e in app.exception])
        return app

    def test_document_context_is_inspected_and_each_call_is_independent(self):
        app = self.app(20)
        self.assertEqual(self.requests, [])
        app.button[0].click().run()
        self.assertEqual(app.session_state['document_result']['answer']['status'], 'insufficient')
        self.assertEqual(json.loads(self.requests[-1]['messages'][-1]['content'])['fragmentos'], [])
        app.radio[0].set_value('Buscar fragmentos').run()
        self.assertTrue(app.info)
        app.button[0].click().run()
        record = app.session_state['document_result']
        self.assertEqual(record['answer']['status'], 'supported')
        self.assertEqual(record['chunks'], json.loads(self.requests[-1]['messages'][-1]['content'])['fragmentos'])
        self.assertTrue(any(e.label.startswith('Fuente citada:') for e in app.expander))
        app.radio[0].set_value('Sin documentos').run()
        app.button[0].click().run()
        self.assertEqual(app.session_state['document_result']['answer']['status'], 'insufficient')
        self.assertTrue(all(len(r['messages']) == 2 for r in self.requests))
        self.assertEqual(len(self.requests), 3)

    def test_document_upload_can_be_excluded_and_invalid_source_ids_are_rejected(self):
        file = BytesIO('Regla ficticia: las taquillas violetas usan el código tulipán.'.encode())
        file.name = 'taquillas.txt'
        with patch('streamlit.file_uploader', return_value=[file]):
            app = self.app(20)
            self.assertIn('taquillas.txt', app.multiselect[0].value)
            app.radio[0].set_value('Todos los fragmentos').run()
            app.button[0].click().run()
            self.assertIn('taquillas.txt', {c['file'] for c in app.session_state['document_result']['chunks']})
            app.multiselect[0].set_value([v for v in app.multiselect[0].value if v != 'taquillas.txt']).run()
            app.button[0].click().run()
            self.assertNotIn('taquillas.txt', {c['file'] for c in app.session_state['document_result']['chunks']})
        self.bad_citation = True
        with self.assertRaisesRegex(ValueError, 'no recibió'):
            answer_documents(openai.OpenAI(), 'baja', load_course_documents(ROOT / 'data/conocimiento'), 'gpt-4.1-mini')

    def test_chart_and_underlying_table_survive_followup_rerun_and_restore(self):
        app = self.app(21)
        app.chat_input[0].set_value('Dibuja el churn mensual por plan en 2024').run(timeout=30)
        self.assertFalse(app.exception, [e.message for e in app.exception])
        self.assertEqual(len(app.get('vega_lite_chart')), 1)
        self.assertEqual(len(app.dataframe), 1)
        self.assertEqual(len(app.dataframe[0].value), 36)
        self.assertEqual(self.requests[-1]['messages'][-1]['role'], 'tool')
        self.assertEqual(self.requests[-1]['messages'][-1]['tool_call_id'], 'call_1')
        self.chart_args['kind'] = 'bar'
        app.chat_input[0].set_value('Ahora en barras').run(timeout=30)
        app.run()
        self.assertFalse(app.exception, [e.message for e in app.exception])
        self.assertEqual(len(app.get('vega_lite_chart')), 2)
        self.assertEqual(len(app.dataframe), 2)
        self.assertEqual(len(self.requests), 4)
        self.assertEqual([m['content'] for m in self.requests[2]['messages'] if m['role'] == 'user'],
                         ['Dibuja el churn mensual por plan en 2024', 'Ahora en barras'])
        fresh = self.app(21)
        fresh.session_state['chart_chat'] = import_history(export_history(app.session_state['chart_chat']).encode())
        fresh.run()
        self.assertEqual(len(fresh.get('vega_lite_chart')), 2)
        self.assertEqual(len(self.requests), 4)

    def test_chart_error_keeps_prior_turns_and_does_not_fake_a_chart(self):
        app = self.app(21)
        self.chart_args['start_month'] = '2030-01'
        app.chat_input[0].set_value('Grafica 2030').run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.chat_message), 2)
        self.assertIn('No se ha completado', app.chat_message[-1].markdown[0].value)
        self.assertEqual(len(app.get('vega_lite_chart')), 0)
        self.denied = True
        app.chat_input[0].set_value('Otra pregunta').run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.chat_message), 4)

    def test_deployment_selector_serves_documents_and_charts_after_authentication(self):
        with patch.dict(os.environ, {'WORKSHOP_PASSWORD': 'test-class'}):
            app = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=30)
            self.assertFalse(app.exception)
            self.assertEqual(len(app.radio), 0)
            app.text_input[0].set_value('test-class').run()
            app.button[0].click().run()
            app.radio[0].set_value('Documentos').run()
            self.assertFalse(app.exception, [e.message for e in app.exception])
            app.radio[1].set_value('Buscar fragmentos').run()
            app.button[0].click().run()
            self.assertEqual(app.session_state['document_result']['answer']['status'], 'supported')
            app.radio[0].set_value('Gráficos').run()
            app.chat_input[0].set_value('Churn mensual por plan en 2024').run()
            self.assertFalse(app.exception, [e.message for e in app.exception])
            self.assertEqual(len(app.get('vega_lite_chart')), 1)
            app.radio[0].set_value('Cálculos').run()
            self.assertEqual(len(app.chat_message), 0)
            app.radio[0].set_value('Gráficos').run()
            self.assertEqual(len(app.get('vega_lite_chart')), 1)
            self.assertEqual(len(self.requests), 3)
