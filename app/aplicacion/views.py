from django.forms.widgets import DateInput
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Dieta, Producto, Usuario
from django.http import HttpResponseRedirect
from .forms import ProductoForm, RegistroForm, LoginForm, UsuarioForm, BusquedaForm, DietaForm
import json
import csv
import pandas as pd
from datetime import datetime
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_activo = request.user.usuario
        return render(request, 'index.html', {'login': user_activo})
    else:
        return render(request, 'index.html')

def lista_productos(request):
    productos = Producto.objects.get_queryset().order_by('nombre')
    if request.user.is_authenticated:
        user_activo = request.user.usuario
        paginator = Paginator(productos, 25) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'lista_productos.html', {'page_obj': page_obj,'productos': productos, 'login': user_activo})

    else:
        paginator = Paginator(productos, 25) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'lista_productos.html', {'page_obj': page_obj,'productos': productos})

def productos_detalle(request, pk):

    try:
        id_producto=Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        raise ("Producto no existe")

    if request.user.is_authenticated:
        user_activo = request.user.usuario

        return render(request,'productos_detalle.html',context={'producto':id_producto, 'login': user_activo})
    else:
        return render(request,'productos_detalle.html',context={'producto':id_producto,})

@login_required
def aniadir_producto(request):
    user_activo = request.user.usuario
    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/lista_productos/')

    else:
        form = ProductoForm()

    return render(request, 'añadir_producto.html', {'form': form, 'login': user_activo})


def login(request):
    form = AuthenticationForm(request=request, data=request.POST)
    username = form.cleaned_data.post('username')
    password = form.cleaned_data.post('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    form = AuthenticationForm()
    return render(request,"login.html",context={"form":form})


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST,request.FILES)

        if form.is_valid():
            user = form.get_user_model()
            login(request, user)
            return render(request, 'index.html', {'usuario': user})
    else:
        form = UserCreationForm()

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
def modificar_producto(request, id_producto):
    user_activo = request.user.usuario
    producto = Producto.objects.filter(id=id_producto).first()
    data = {producto.nombre, producto.calorias, producto.proteinas, producto.grasa}
    form = ProductoForm(data)
    return render(request, 'modificar_producto.html', {'form': form, 'login': user_activo})


@login_required
def borrar_producto(request, id_producto):
    Producto.objects.filter(id=id_producto).delete()
    return redirect('/lista_productos/')

@login_required
def mostrar_perfil(request):
    user_activo = request.user.usuario
    usuario = Usuario.objects.filter(email=request.POST.get('email'))
    return render(request,'mostrar_perfil.html', context={'usuario':usuario, 'login': user_activo})

@login_required
def modificar_perfil(request):
    user_activo = request.user.usuario
    if request.method == 'POST' and 'modificado' in request.POST:
        nombre = request.user.nombre
        apellidos = request.user.apellidos
        fecha_nacimiento = request.user.fecha_nacimiento
        genero = request.user.genero
        altura = request.user.altura
        peso = request.user.peso
        Usuario.objects.filter(email=request.user.email).update(nombre=nombre, apellidos=apellidos, fecha_nacimiento=fecha_nacimiento, genero=genero, altura=altura, peso=peso)
        usuario = Usuario.objects.filter(email=request.user.email)
        return render(request, 'mostrar_perfil.html', {'usuario': usuario, 'login': user_activo})

    else:
        usuario = Usuario.objects.filter(email=request.POST.get('email_modificar'))
        form = UsuarioForm()
        return render(request, 'modificar_perfil.html', {'form': form, 'login': user_activo})

@login_required
def borrar_perfil(request):
    Usuario.objects.filter(email=request.POST.get('email_borrar')).delete()
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
    if(request.user.is_staff):
        dieta = Dieta.objects.all()
    else:
        dieta = Dieta.objects.filter(usuario=user_activo.usuario)
    return render(request,'mostrar_dieta.html', context={'dieta':dieta, 'login': user_activo})
