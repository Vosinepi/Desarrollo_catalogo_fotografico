from django.test import TestCase

from .models import Contacto

# Create your tests here.


class ContactoTestCase(TestCase):
    def setUp(self):
        Contacto.objects.create(
            nombre="Juan",
            apellido="Perez",
            email="jua@juan.com",
            subject="Prueba",
            menssage="Prueba",
        )

    def test_contacto_cread(self):
        contacto = Contacto.objects.get(nombre="Juan")
        self.assertEqual(contacto.nombre, "Juan")
        self.assertEqual(contacto.apellido, "Perez")
