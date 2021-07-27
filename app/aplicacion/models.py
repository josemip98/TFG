from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.urls import reverse

# Create your models here.

class UsuarioManager(BaseUserManager):
  def create_user(self,email,usuario,nombre,apellidos,password):
    if not email:
      raise ValueError('El usuario debe tener un correo electrónico')

    user = self.model(
        usuario = usuario,
        email = self.normalize_email(email),
        nombre = nombre,
        apellidos = apellidos,
        password = password
    )

    user.save()
    return user

  def create_superuser(self,usuario,email,nombre,apellidos,password):
    user = self.create_user(
      email,
      usuario=usuario,
      nombre=nombre,
      apellidos = apellidos,
      password = password
    )
    user.administrador = True
    user.save()
    return user

class Usuario(AbstractBaseUser):
  id = models.AutoField(primary_key=True)
  usuario = models.CharField('Usuario', max_length=200, unique=True)
  email = models.EmailField('Email', max_length=200, unique=True)
  nombre = models.CharField(max_length=200, null=False)
  apellidos = models.CharField(max_length=200, null=True)
  fecha_nacimiento = models.DateField(blank=True, null=True)
  genero = models.CharField(max_length=10, null=True)
  altura = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  peso = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  imagen = models.ImageField('Imagen de perfil', upload_to='perfil/', height_field=None, width_field=None, max_length=200, null=True)
  administrador = models.BooleanField(default=False)
  activo = models.BooleanField(default=True)
  created_on = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
  updated_on = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True)
  objects = UsuarioManager()

  USERNAME_FIELD = 'usuario'
  REQUIRED_FIELDS = ['email', 'nombre', 'apellidos']

  def __str__(self):
    return f'{self.nombre}'

  def has_perm(self,perm,obj = None):
    return True
  
  def has_module_perms(self,aplicacion):
    return True
  
  @property
  def is_staff(self):
    return self.administrador

class Producto(models.Model):
  id = models.AutoField(primary_key=True)
  nombre = models.CharField(max_length=100, unique=True)
  marca = models.CharField(max_length=100, null=True)
  categoria = models.TextField(null=True)
  tienda = models.CharField(max_length=200, null=True)
  pais = models.CharField(max_length=100, null=True)
  ingredientes = models.TextField(null=True)
  alergenos = models.TextField(null=True)
  aditivos = models.TextField(null=True)
  puntuacion_nova = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  image_url = models.CharField(max_length=200, null=True)
  image_small_url = models.CharField(max_length=200, null=True)
  calorias = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  energia = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  grasa = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  grasas_saturadas = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  colesterol = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  carbohidratos = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  azucares = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  fibra = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  proteinas = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  sal = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  sodio = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  calcio = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  hierro = models.DecimalField(max_digits=10,decimal_places=5,blank=True, null=True)
  puntuacion = models.IntegerField(blank=True, null=True)

  REQUIRED_FIELDS = ['nombre', 'calorias', 'grasa', 'proteinas']

  def get_absolute_url(self):
    return reverse('productos_detalle', args=[str(self.id)])

  def __str__(self):
    return self.nombre

class Dieta(models.Model):
  id = models.AutoField(primary_key=True)
  nombre = models.CharField(max_length=200, null=True)
  descripcion = models.TextField(max_length=200, null=True)
  productos = models.ManyToManyField(Producto)
  usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return self.nombre

  def get_productos(self):
    return ", ".join([p.nombre for p in self.productos.all()])