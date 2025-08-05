import unittest

from app.services.base_handler import agregar_registro, obtener_registro
from app.common.db.unit_of_work import DEFAULT_SESSION_FACTORY

from unit_test.random_stuff import random_string

class TestDemoUnitOfWork(unittest.TestCase):
    def setUp(self):
        self.session = DEFAULT_SESSION_FACTORY(expire_on_commit=False)

    def get_name_and_message(self):
        return random_string('nombre '), random_string('mensaje ')

    def get_user(self, id:int):
        [[nombre]] = self.session.execute(
            "SELECT C_TipoInstitucion FROM tbc_hawk_alert WHERE idHawkAlert=:id",
            dict(id=id)
        )
        return nombre

    def test_agregar_registro(self):
        name, mensaje = self.get_name_and_message()
        test_id = agregar_registro(name, mensaje)
        expected_name = self.get_user(test_id)

        self.assertEqual(expected_name, name)

    def test_obtener_registro(self):
        name, message = self.get_name_and_message()
        test_id = agregar_registro(name, message)
        user = obtener_registro(test_id)

        self.assertEqual(user.TipoInstitucion, name)

        