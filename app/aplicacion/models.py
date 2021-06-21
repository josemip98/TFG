from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Usuario(models.Model):
  id = models.AutoField(primary_key=True)
  nombre = models.CharField(max_length=200)
  apellidos = models.CharField(max_length=200)
  email = models.CharField(max_length=200, unique=True)

  def __str__(self):
    return self.nombre

class Producto(models.Model):
  id = models.AutoField(primary_key=True)
  nombre = models.CharField(max_length=200)
  marca = models.CharField(max_length=200)
  calorias = models.CharField(max_length=200)
  hidratos = models.CharField(max_length=200)
  grasa = models.CharField(max_length=200)
  proteinas = models.CharField(max_length=200)

  def get_absolute_url(self):
    return reverse('productos_detalle', args=[str(self.id)])

  def __str__(self):
    return self.nombre

#class Dieta(models.Model):
#  productos = models.ArrayField(Producto)

#  def __str__(self):
#    return self.productos

