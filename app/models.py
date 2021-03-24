from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
  nombre = models.CharField(max_length=200)

  def __str__(self):
    return self.nombre

class Producto(models.Model):
  nombre = models.CharField(max_length=200)
  imagen = models.ImageField(upload_to ='productos', blank=True)
  marca = models.CharField(max_length=200)
  calorias = models.CharField(max_length=200)
  hidratos = models.CharField(max_length=200)
  grasa = models.CharField(max_length=200)
  proteinas = models.CharField(max_length=200)

  def __str__(self):
    return self.nombre

#class Dieta(models.Model):
#  productos = models.ArrayField(Producto)

#  def __str__(self):
#    return self.productos

