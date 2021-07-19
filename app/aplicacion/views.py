from django.forms.widgets import DateInput
from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Dieta, Producto, Usuario
from django.http import HttpResponseRedirect
from .forms import ProductoForm, RegistroForm, LoginForm, UsuarioForm, BusquedaForm, DietaForm
import json
import csv
import pandas as pd
from datetime import datetime


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_activo = request.user.usuario
        return render(request, 'index.html', {'login': user_activo})
    else:
        return render(request, 'index.html')

def lista_productos(request):
    user_activo = request.user.usuario
    # df = pd.read_csv("data/nutrition.csv")
  
    # parsing the DataFrame in json format.
    #json_records = df.reset_index().to_json(orient ='records')
    #data = []
    #data = json.loads(json_records)
    productos = Producto.objects.all()
    context = {'login': user_activo,'productos': productos}

    if request.user.is_authenticated:
        return render(request, 'lista_productos.html', context)

    else:
        return render(request, 'lista_productos.html', context)

def productos_detalle(request, pk):
    user_activo = request.user.usuario
    try:
        producto_id=Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        raise ("Producto no existe")

    return render(
        request,
        'productos_detalle.html',
        context={'producto':producto_id, 'login': user_activo}
    )

@login_required
def aniadir_producto(request):
    user_activo = request.user.usuario
    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            form.save()
            productos = Producto.objects.all()
            return render(request, 'lista_productos.html', {'productos': productos, 'login': user_activo})

    else:
        form = ProductoForm()

    return render(request, 'añadir_producto.html', {'form': form, 'login': user_activo})


def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(usuario=request.POST['username'],password=request.POST['password'])

            if user is not None:
                do_login(request, user)
                return render(request, "index.html", {'login': usuario})
    return render(request, "login.html", {'form': form})


def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            productos = Producto.objects.all()
            return render(request, 'index.html', {'productos': productos})
    else:
        form = UsuarioForm()

    return render(request, 'registro.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)

def buscar_producto(request):
    user_activo = request.user.usuario
    if request.method == 'POST' and 'buscar' in request.POST:
        producto = Producto.objects.get('nombre')
        return render(request, 'productos_detalle.html', {'producto': producto, 'login': user_activo})
    else:
        form = BusquedaForm()
        return render(request, 'buscar_producto.html', {'form': form, 'login': user_activo})

@login_required
def modificar_producto(request):
    user_activo = request.user.usuario
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
        data = {producto.nombre, producto.marca, producto.calorias, producto.hidratos, producto.grasa, producto.proteinas}
        form = ProductoForm(data)
        return render(request, 'modificar_producto.html', {'form': form, 'login': user_activo})


@login_required
def borrar_producto(request):
    user_activo = request.user.usuario
    Producto.objects.filter(nombre=request.POST.get('titulo_borrar')).delete()
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos, 'login': user_activo})

@login_required
def mostrar_perfil(request):
    user_activo = request.user.usuario
    usuario = Usuario.objects.filter(email=request.POST.get('email'))
    return render(request,'mostrar_perfil.html', context={'usuario':usuario, 'login': user_activo})

@login_required
def modificar_perfil(request):
    user_activo = request.user.usuario
    if request.method == 'POST' and 'modificado' in request.POST:
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        genero = request.POST.get('genero')
        altura = request.POST.get('altura')
        peso = request.POST.get('peso')
        Usuario.objects.filter(email=request.user.email).update(nombre=nombre, apellidos=apellidos, fecha_nacimiento=fecha_nacimiento, genero=genero, altura=altura, peso=peso)
        usuario = Usuario.objects.filter(email=request.user.email)
        return render(request, 'mostrar_perfil.html', {'usuario': usuario, 'login': user_activo})

    else:
        usuario = Usuario.objects.filter(email=request.POST.get('email_modificar'))
        form = UsuarioForm()
        return render(request, 'modificar_perfil.html', {'form': form, 'login': user_activo})

@login_required
def borrar_perfil(request):
    user_activo = request.user.usuario
    User.objects.filter(email=request.POST.get('email_borrar')).delete()
    return render(request, 'index.html')

@login_required
def aniadir_dieta(request):
    user_activo = request.user.usuario
    if request.method == 'POST':
        form = DietaForm(request.POST)

        if form.is_valid():
            form.save()
            dieta = Dieta.objects.all()
            return render(request, 'mostrar_dieta.html', {'dieta': dieta, 'login': user_activo})

    else:
        form = DietaForm()

    return render(request, 'añadir_dieta.html', {'form': form, 'login': user_activo})

@login_required
def mostrar_dieta(request):
    user_activo = request.user.usuario
    dieta = Dieta.objects.all()
    return render(request,'mostrar_dieta.html', context={'dieta':dieta, 'login': user_activo})
