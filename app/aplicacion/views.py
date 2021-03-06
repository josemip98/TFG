from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as do_login
from django.core.paginator import Paginator
from .models import Dieta, Producto, Usuario
from django.http import HttpResponseRedirect
from .forms import ProductoForm, LoginForm, UsuarioForm, ContactoForm, DietaForm
import random
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from django.db.models import Q

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_activo = request.user.usuario
        return render(request, 'index.html', {'login': user_activo})
    else:
        form = LoginForm(request.POST)
        return render(request,"index.html",context={"form":form})

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

def buscar_productos_similares(producto):
    querys = (Q(proteinas__icontains=producto.proteinas) | Q(grasa__icontains=producto.grasa) & ~Q(nombre__icontains=producto.nombre))
    productos = Producto.objects.get_queryset().order_by('calorias').filter(querys)
    return productos

def productos_detalle(request, pk):
    try:
        producto=Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        raise ("Producto no existe")
    if request.user.is_authenticated:
        user_activo = request.user.usuario
    if(producto.calorias != None and producto.grasa != None):
        productos = buscar_productos_similares(producto)  
        return render(request,'productos_detalle.html',context={'producto':producto, 'login': user_activo, 'productos': productos})
    else:
        return render(request,'productos_detalle.html',context={'producto':producto,})

def contacto(request):
    form = ContactoForm()
    if request.user.is_authenticated:
        user_activo = request.user.usuario
        return render(request, 'contacto.html', {'login': user_activo, 'form': form})
    else:
        return render(request, 'contacto.html', {'form': form})

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
    return render(request, 'a??adir_producto.html', {'form': form, 'login': user_activo})


def login(request):
    form = LoginForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            do_login(request,user)
            return redirect('index')
        else:
            form = LoginForm(request.POST)
            return render(request,"login.html",context={"form":form})
    else:
        form = LoginForm(request.POST)
        return render(request,"login.html",context={"form":form})


def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST,request.FILES)
        if form.is_valid():
            username = request.POST['usuario']
            password = request.POST['password']
            password = make_password(password)
            email = request.POST['email']
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            genero = request.POST['genero']
            usuario = Usuario.objects.create(usuario=username, password=password, email=email, nombre=nombre, apellidos=apellidos, genero=genero)
            usuario.save()
            do_login(request, usuario)
            return render(request, 'base.html', {'usuario': usuario})
        else:
            form = UsuarioForm()
            return render(request, 'registro.html', {'form': form})
    else:
        form = UsuarioForm()
        return render(request, 'registro.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)

def buscar_producto(request):
    producto = request.GET.get('producto', '')
    querys = Q(nombre__icontains=producto)
    productos = Producto.objects.get_queryset().order_by('nombre').filter(querys)
    paginator = Paginator(productos, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        user_activo = request.user.usuario
        return render(request,'lista_productos.html',{'productos':productos, 'page_obj': page_obj, 'login': user_activo})
    else:
        return render(request,'lista_productos.html',{'productos':productos, 'page_obj': page_obj,})

@login_required
def modificar_producto(request, id_producto):
    user_activo = request.user.usuario
    if request.method == 'POST' and 'modificado' in request.POST:
        nombre = request.POST['nombre']
        marca = request.POST['marca']
        tienda = request.POST['tienda']
        pais = request.POST['pais']
        alergenos = request.POST['alergenos']
        aditivos = request.POST['aditivos']
        puntuacion_nova = request.POST['puntuacion_nova']
        calorias = request.POST['calorias']
        energia = request.POST['energia']
        grasa = request.POST['grasa']
        grasas_saturadas = request.POST['grasas_saturadas']
        colesterol = request.POST['colesterol']
        carbohidratos = request.POST['carbohidratos']
        azucares = request.POST['azucares']
        fibra = request.POST['fibra']
        proteinas = request.POST['proteinas']
        sal = request.POST['sal']
        sodio = request.POST['sodio']
        calcio = request.POST['calcio']
        hierro = request.POST['hierro']
        puntuacion = request.POST['puntuacion']
        Producto.objects.filter(id=id_producto).update(nombre=nombre, marca=marca, tienda=tienda, pais=pais, alergenos=alergenos, 
        aditivos=aditivos, puntuacion_nova=puntuacion_nova, calorias=Decimal(calorias), energia=Decimal(energia), grasa=Decimal(grasa),
        grasas_saturadas=Decimal(grasas_saturadas), colesterol=Decimal(colesterol), carbohidratos=Decimal(carbohidratos), azucares=Decimal(azucares), fibra=Decimal(fibra),
        proteinas=Decimal(proteinas), sal=Decimal(sal), sodio=Decimal(sodio), calcio=Decimal(calcio), hierro=Decimal(hierro), puntuacion=puntuacion)
        return redirect('lista_productos')

    else:
        form = ProductoForm()
        producto = Producto.objects.get(id=id_producto)
        return render(request, 'modificar_producto.html', {'form': form, 'login': user_activo, 'producto': producto})


@login_required
def borrar_producto(request, id_producto):
    Producto.objects.filter(id=id_producto).delete()
    return redirect('/lista_productos/')

@login_required
def mostrar_perfil(request):
    user_activo = request.user.usuario
    usuario = Usuario.objects.get(id=request.user.id)
    return render(request,'mostrar_perfil.html', context={'usuario':usuario, 'login': user_activo})

@login_required
def modificar_perfil(request, id_usuario):
    user_activo = request.user.usuario
    if request.method == 'POST' and 'modificado' in request.POST:
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        fecha_nacimiento = request.POST['fecha_nacimiento']
        genero = request.POST['genero']
        altura = request.POST['altura']
        peso = request.POST['peso']
        Usuario.objects.filter(id=id_usuario).update(nombre=nombre, apellidos=apellidos, fecha_nacimiento=fecha_nacimiento, genero=genero, altura=altura, peso=peso)
        return redirect('/mostrar_perfil/')

    else:
        form = UsuarioForm()
        return render(request, 'modificar_perfil.html', {'form': form, 'login': user_activo})

@login_required
def borrar_perfil(request):
    Usuario.objects.filter(email=request.POST.get('email_borrar')).delete()
    return render(request, 'base.html')

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

    return render(request, 'a??adir_dieta.html', {'form': form, 'login': user_activo})

@login_required
def mostrar_dieta(request):
    user_activo = request.user.usuario
    if(request.user.is_staff):
        dieta = Dieta.objects.all()
    else:
        dieta = Dieta.objects.filter(usuario=request.user.id)

    return render(request,'mostrar_dieta.html', context={'dieta':dieta, 'login': user_activo})

@login_required
def ver_dieta(request, id_dieta):
    user_activo = request.user.usuario

    dieta = Dieta.objects.get(id=id_dieta)

    if dieta is not None:
        return render(request,'ver_dieta.html', {'dieta':dieta, 'login': user_activo})
    else:
        return render(request,'mostrar_dieta.html', {'dieta':dieta, 'login': user_activo})

@login_required
def generar_dieta(request):
    user_activo = request.user.usuario
    if request.method == 'POST' and 'crear_dieta' in request.POST:
        objetivo = request.POST['objetivo']
        if(objetivo=="1"):
            dieta = Dieta.objects.create(nombre="Volumen",descripcion="Dieta para ganar volumen", usuario=request.user)
            dieta.save()
            items = list(Producto.objects.all())
            random_items = random.sample(items, 10)
            for p in random_items:
                producto = Producto.objects.get(id=p.id)
                dieta.productos.add(producto.id)
        elif(objetivo=="2"):
            dieta = Dieta.objects.create(nombre="Perder peso",descripcion="Dieta para perder peso", usuario=request.user)
            dieta.save()
            items = list(Producto.objects.all())
            random_items = random.sample(items, 10)
            for p in range(10):
                producto = Producto.objects.get(id=p.id)
                dieta.productos.add(producto.id)
        else:
            items = list(Producto.objects.all())
            random_items = random.sample(items, 10)
            dieta = Dieta.objects.create(nombre="Dieta aleatoria",descripcion="Aleatoria", usuario=request.user)
            dieta.save()
            for p in random_items:
                producto = Producto.objects.get(id=p.id)
                dieta.productos.add(producto.id)
        return redirect('/mostrar_dieta/')
    else:
        return render(request,'generar_dieta.html', {'login': user_activo})

@login_required
def export_pdf(request):
    user_activo = request.user.usuario
    return render(request,'mostrar_dieta.html', {'login': user_activo})