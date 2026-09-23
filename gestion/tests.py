from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Cliente, Cuenta, Etiqueta, Transaccion


class ClienteTest(TestCase):
#prueba Que podemos crear un cliente
    def test_crear_cliente(self):
        cliente = Cliente.objects.create(
            nombre="Cliente Prueba",
            email="cliente@prueba.cl",
            telefono="123456789"
        )

        self.assertEqual(cliente.nombre, "Cliente Prueba")
        self.assertEqual(cliente.email, "cliente@prueba.cl")


class CuentaTest(TestCase):
#prueba que una cuenta pertenece a un cliente, Relación OneToOne
    def test_cuenta_pertenece_a_cliente(self):
        cliente = Cliente.objects.create(
            nombre="Cliente Prueba",
            email="cliente@prueba.cl"
        )

        cuenta = Cuenta.objects.create(
            cliente=cliente,
            numero_cuenta="TEST001",
            saldo=100000
        )

        self.assertEqual(cuenta.cliente, cliente)
        self.assertEqual(cliente.cuenta, cuenta)


class TransaccionTest(TestCase):
#prueba que una transaccion pertenece a una cuenta, Relación ForeignKey
    def test_transaccion_pertenece_a_cuenta(self):
        cliente = Cliente.objects.create(
            nombre="Cliente Prueba",
            email="cliente@prueba.cl"
        )

        cuenta = Cuenta.objects.create(
            cliente=cliente,
            numero_cuenta="TEST002",
            saldo=100000
        )

        transaccion = Transaccion.objects.create(
            cuenta=cuenta,
            tipo="INGRESO",
            monto=50000
        )

        self.assertEqual(transaccion.cuenta, cuenta)
        self.assertEqual(cuenta.transacciones.first(), transaccion)


class EtiquetaTest(TestCase):
#prueba que una transaccion puede tener varias etiquetas y una etiqueta puede estar en varias transacciones, Relación ManyToMany
    def test_transaccion_puede_tener_etiquetas(self):
        cliente = Cliente.objects.create(
            nombre="Cliente Prueba",
            email="cliente@prueba.cl"
        )

        cuenta = Cuenta.objects.create(
            cliente=cliente,
            numero_cuenta="TEST003",
            saldo=100000
        )

        transaccion = Transaccion.objects.create(
            cuenta=cuenta,
            tipo="GASTO",
            monto=10000
        )

        alimentacion = Etiqueta.objects.create(nombre="Alimentación")
        hogar = Etiqueta.objects.create(nombre="Hogar")

        transaccion.etiquetas.add(alimentacion, hogar)

        self.assertEqual(transaccion.etiquetas.count(), 2)
        self.assertIn(alimentacion, transaccion.etiquetas.all())
        self.assertIn(hogar, transaccion.etiquetas.all())


class ValidacionTest(TestCase):
#prueba que el monto de una transaccion no puede ser cero.Validacion monto minimo
    def test_monto_no_puede_ser_cero(self):
        cliente = Cliente.objects.create(
            nombre="Cliente Prueba",
            email="cliente@prueba.cl"
        )

        cuenta = Cuenta.objects.create(
            cliente=cliente,
            numero_cuenta="TEST004",
            saldo=100000
        )

        transaccion = Transaccion(
            cuenta=cuenta,
            tipo="INGRESO",
            monto=0
        )

        with self.assertRaises(ValidationError):
            transaccion.full_clean()