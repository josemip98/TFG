from django import forms
from django.contrib.auth.models import User
from .models import Producto, Usuario, Dieta

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields = ('usuario','email','password', 'nombre','apellidos','fecha_nacimiento','genero','altura','peso','imagen')

class ProductoForm(forms.ModelForm):
    marca = forms.CharField(required=False)
    pais = forms.CharField(required=False)
    ingredientes = forms.CharField(required=False)
    alergenos = forms.CharField(required=False)
    trazas = forms.CharField(required=False)
    cantidad_servicio = forms.CharField(required=False)
    aditivos = forms.CharField(required=False)
    categoria = forms.CharField(required=False)
    image_url = forms.CharField(required=False)
    image_small_url = forms.CharField(required=False)
    grasas_saturadas = forms.CharField(required=False)
    grasas_trans = forms.CharField(required=False)
    colesterol = forms.CharField(required=False)
    carbohidratos = forms.CharField(required=False)
    azucares = forms.CharField(required=False)
    fibra = forms.CharField(required=False)
    sal = forms.CharField(required=False)
    sodio = forms.CharField(required=False)
    calcio = forms.CharField(required=False)
    hierro = forms.CharField(required=False)
    puntuacion = forms.CharField(required=False)

    class Meta:
        model = Producto
        fields = ('nombre','marca','tienda', 'pais','alergenos','cantidad_servicio','aditivos','puntuacion_nova','image_url','image_small_url','calorias','energia','grasa','grasas_saturadas','grasas_trans','colesterol','carbohidratos','azucares','fibra','proteinas','sal','sodio','calcio','hierro','puntuacion')

class DietaForm(forms.ModelForm):
    nombre = forms.CharField(required=False)
    descripcion = forms.CharField(required=False)

    class Meta:
        model = Dieta
        fields = ('nombre','descripcion','productos','usuario')

class RegistroForm(forms.ModelForm):
    class Meta:
        password = forms.CharField(widget = forms.PasswordInput)
        model = User
        widgets = {'password': forms.PasswordInput()}
        fields = ('username', 'password', 'email', 'first_name', 'last_name',)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))

class LoginForm(forms.Form):
     username = forms.CharField(max_length=150)
     password = forms.CharField(widget = forms.PasswordInput)

class BusquedaForm(forms.Form):
     nombre = forms.CharField(max_length=150)
