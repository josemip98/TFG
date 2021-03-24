from django import forms
from django.contrib.auth.models import User
from .models import Producto, Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nombre',)

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre','imagen', 'marca', 'calorias', 'hidratos', 'grasa', 'proteinas')

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
