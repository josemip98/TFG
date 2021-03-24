from django.shortcuts import render, HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Producto, Usuario
from .forms import ProductoForm, RegistroForm, LoginForm, UsuarioForm
import json

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        user_activo = request.user.username
        return render(request, 'index.html', {'login': user_activo})
    else:
        context = {'username': None}
        return render(request, 'index.html', context)


def test_template(request):
    context = {}
    return render(request, 'test.html', context)


def lista_productos(request):
    productos = Producto.objects.all()

    if request.user.is_authenticated:
        user_activo = request.user.username
        return render(request, 'lista_productos.html', {'login': user_activo, 'productos': productos})

    else:
        return render(request, 'lista_productos.html', {'productos': productos})


@login_required
def producto(request):
    user_activo = request.user.username
    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            form.save()
            productos = Producto.objects.all()
            return render(request, 'lista_productos.html', {'productos': productos, 'login': user_activo})

    else:
        form = ProductoForm()

    return render(request, 'producto.html', {'form': form, 'login': user_activo})


def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                return render(request, "index.html", {'login': username})

    return render(request, "login.html", {'form': form})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            productos = Producto.objects.all()
            return render(request, 'index.html', {'productos': productos})

    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'index.html')

def buscar_producto(request):
    user_activo = request.user.username
    if request.method == 'POST' and 'buscar' in request.POST:
        id = request.POST.get('id')
        nombre = request.POST.get('nombre')
        marca = request.POST.get('marca')
        calorias = request.POST.get('calorias')
        hidratos = request.POST.get('hidratos')
        grasa = request.POST.get('grasa')
        proteinas = request.POST.get('proteinas')
        Producto.objects.filter(nombre=nombre)
        productos = Producto.objects.all()
        return render(request, 'lista_productos.html', {'productos': productos, 'login': user_activo})

    else:
        form = ProductoForm()
        return render(request, 'buscar_producto.html', {'form': form, 'login': user_activo})

@login_required
def modificar_producto(request):
    user_activo = request.user.username
    if request.method == 'POST' and 'modificado' in request.POST:
        id = request.POST.get('id')
        nombre = request.POST.get('nombre')
        marca = request.POST.get('marca')
        calorias = request.POST.get('calorias')
        hidratos = request.POST.get('hidratos')
        grasa = request.POST.get('grasa')
        proteinas = request.POST.get('proteinas')
        Producto.objects.filter(id=id).update(
            nombre='nombre', marca='marca', calorias='calorias', hidratos='hidratos', grasa='grasa', proteinas='proteinas')
        productos = Producto.objects.all()
        return render(request, 'lista_productos.html', {'productos': productos, 'login': user_activo})

    else:
        producto = Producto.objects.filter(nombre=request.POST.get('nombre_modificar'))
        data = {'nombre': producto.nombre,'imagen': producto.imagen, 'marca': producto.marca, 'calorias': producto.calorias, 'hidratos': producto.hidratos, 'grasa': producto.grasa, 'proteinas': producto.proteinas}
        form = ProductoForm(data)
        return render(request, 'modificar_producto.html', {'form': form, 'login': user_activo})


@login_required
def borrar_producto(request):
    user_activo = request.user.username
    Producto.objects.filter(nombre=request.POST.get('titulo_borrar')).delete()
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos, 'login': user_activo})
