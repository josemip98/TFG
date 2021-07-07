from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Producto, Usuario
from django.http import HttpResponseRedirect
from .forms import ProductoForm, RegistroForm, LoginForm, UsuarioForm, BusquedaForm
import json
import csv
import pandas as pd


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_activo = request.user.username
        return render(request, 'index.html', {'login': user_activo})
    else:
        return render(request, 'index.html')

def lista_productos(request):
    user_activo = request.user.username
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
    user_activo = request.user.username
    try:
        producto_id=Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        raise Http404("Producto no existe")

    return render(
        request,
        'productos_detalle.html',
        context={'producto':producto_id, 'login': user_activo}
    )

@login_required()
def aniadir_producto(request):
    user_activo = request.user.username
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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                return render(request, "index.html", {'login': username})

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
    user_activo = request.user.username
    if request.method == 'POST' and 'buscar' in request.POST:
        producto = Producto.objects.get('nombre')
        return render(request, 'productos_detalle.html', {'producto': producto, 'login': user_activo})
    else:
        form = BusquedaForm()
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
        data = {producto.id, producto.nombre, producto.marca, producto.calorias, producto.hidratos, producto.grasa, producto.proteinas}
        form = ProductoForm(data)
        return render(request, 'modificar_producto.html', {'form': form, 'login': user_activo})


@login_required
def borrar_producto(request):
    user_activo = request.user.username
    Producto.objects.filter(nombre=request.POST.get('titulo_borrar')).delete()
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos, 'login': user_activo})

@login_required
def mostrar_perfil(request):
    user_activo = request.user.username
    email = request.user.email
    return render(request,'mostrar_perfil.html', context={'usuario':request.user, 'login': user_activo})

@login_required
def modificar_perfil(request):
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
        usuario = Usuario.objects.filter(email=request.POST.get('email_modificar'))
        data = {usuario.nombre, usuario.apellidos, usuario.email}
        form = UsuarioForm(data)
        return render(request, 'modificar_perfil.html', {'form': form, 'login': user_activo})


@login_required
def borrar_perfil(request):
    user_activo = request.user.username
    User.objects.filter(email=request.POST.get('email_borrar')).delete()
    return render(request, 'index.html')
