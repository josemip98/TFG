from django.test import TestCase

# Create your tests here.

from .models import Producto

# Tests clase producto
class ProductoModelTest(TestCase):

    @classmethod
    def testCrearProducto(self):
        print("Test crear producto")
        self.test_producto = Producto(nombre="Arroz")
        self.test_producto.save()

    def testModificarProducto(self):
        print("Test modificar producto")
        self.test_producto = Producto(nombre="Arroz", calorias=10, grasa=10, proteinas=10)
        self.test_producto.save()
        Producto.objects.filter(nombre="Arroz").update(calorias=20)