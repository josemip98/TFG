from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse


# Create your models here.

class Usuario(AbstractBaseUser):
  usuario = models.CharField('Usuario', max_length=200, unique=True)
  email = models.EmailField('Email', max_length=200, unique=True)
  nombre = models.CharField(max_length=200)
  apellidos = models.CharField(max_length=200)
  fecha_nacimiento = models.DateField(default=None)
  edad = models.DurationField(default=None)
  genero = models.CharField(max_length=10)
  altura = models.PositiveIntegerField()
  peso = models.PositiveIntegerField()
  imagen = models.ImageField('Imagen de perfil', upload_to='perfil/', height_field=None, width_field=None, max_length=200)
  administrador = models.BooleanField(default=False)
  activo = models.BooleanField(default=True)
  created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
  updated_on = models.DateTimeField(auto_now_add=False, auto_now=True)
  
  USERNAME_FIELD = 'usuario'
  REQUIRED_FIELDS = ['usuario','email']

  def __str__(self):
    return self.usuario

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
