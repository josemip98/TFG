from django import forms
from django.contrib.auth.models import User
from .models import Producto, Usuario, Dieta
from django.conf import settings

class UsuarioForm(forms.ModelForm):
    GENEROS= (
    ('1','Masculino'),
    ('2','Femenino'),
    ('3','Otro'),
    )
    genero = forms.ChoiceField(widget=forms.Select, choices=GENEROS)
    password = forms.CharField(widget=forms.PasswordInput)
    fecha_nacimiento = forms.DateField(
    localize=True,
    widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}),
)
    imagen = forms.DecimalField(required=False)
    class Meta:
        model = Usuario
        fields = ('usuario','email','password', 'nombre','apellidos','fecha_nacimiento','genero','altura','peso','imagen')

class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(required=True)
    calorias = forms.DecimalField(required=True)
    grasa = forms.DecimalField(required=True)
    proteinas = forms.DecimalField(required=True)
    marca = forms.CharField(required=False)
    tienda = forms.CharField(required=False)
    pais = forms.CharField(required=False)
    ingredientes = forms.CharField(required=False)
    alergenos = forms.CharField(required=False)
    trazas = forms.CharField(required=False)
    aditivos = forms.CharField(required=False)
    categoria = forms.CharField(required=False)
    image_url = forms.CharField(required=False)
    image_small_url = forms.CharField(required=False)
    grasas_saturadas = forms.DecimalField(required=False)
    colesterol = forms.DecimalField(required=False)
    carbohidratos = forms.DecimalField(required=False)
    azucares = forms.DecimalField(required=False)
    fibra = forms.DecimalField(required=False)
    sal = forms.DecimalField(required=False)
    sodio = forms.DecimalField(required=False)
    calcio = forms.DecimalField(required=False)
    hierro = forms.DecimalField(required=False)
    puntuacion = forms.DecimalField(required=False)

    class Meta:
        model = Producto
        fields = ('nombre','marca','tienda', 'pais','alergenos','aditivos','puntuacion_nova','image_url','image_small_url','calorias','energia','grasa','grasas_saturadas','colesterol','carbohidratos','azucares','fibra','proteinas','sal','sodio','calcio','hierro','puntuacion')

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
