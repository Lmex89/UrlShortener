from fastapi.testclient import TestClient
from unittest.mock import patch
import unittest

from main import app
from common.config import API_PREFIX
from services import short_code_handler

from unit_test.e2e import api_client
from unit_test.random_stuff import random_string, random_number


id_generado = random_number()
BASE = '/base'

class MockBaseModel:
    def __init__(self, Id, Mensaje):
        self.Id = Id
        self.Mensaje = Mensaje

with TestClient(app) as client:
    class TestApiRoutes(unittest.TestCase):
        def setUp(self):
            self.post_test_path = f'{API_PREFIX}{BASE}/test'
            self.post_add_path = f'{API_PREFIX}{BASE}/add'
            self.get_path = f'{API_PREFIX}{BASE}/get'

        def test_post_test(self):        
            payload = api_client.get_post_test_payload(
                random_string(),
                random_string(),
                random_string()
            )
            expected_response = api_client.get_post_test_response()

            response = client.post(
                self.post_test_path,
                json=payload
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), expected_response)

        @patch.object(short_code_handler, 'agregar_registro', return_value=id_generado)
        def test_post_add(self, mock_agregar_registro):
            payload = api_client.get_post_add_payload(
                random_string('name '),
                random_string('comment ')
            )
            expected_response = api_client.get_post_add_response(
                id_generado
            )

            response = client.post(
                self.post_add_path,
                json=payload
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), expected_response)

        @patch.object(short_code_handler,'obtener_registro',
            return_value=MockBaseModel(
                id_generado,
                'this is a message'
            )
        )
        def test_get_method(self, mock_obtener_registro):
            path = f'{self.get_path}?id={id_generado}'
            expected_response = api_client.get_method_response(
                id_generado,
                'this is a message'
            )
            response = client.get(path)
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), expected_response)