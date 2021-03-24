from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('test_template', views.test_template, name='test_template'),
  path('registro', views.registro, name='registro'),
  path('login', views.login, name='login'),
  path('logout', views.logout_view, name='logout'),
  path('lista_productos', views.lista_productos, name='lista_productos'),
  path('producto', views.producto, name='producto'),
  path('modificar_producto', views.modificar_producto, name='modificar_producto'),
  path('borrar_producto', views.borrar_producto, name='borrar_producto'),
  path('buscar_producto', views.buscar_producto, name='buscar_producto'),
  #path('lista_dietas', views.lista_dietas, name='lista_dietas'),
  #path('dieta', views.dieta, name='dieta'),
  #path('modificar_dieta', views.modificar_dieta, name='modificar_dieta'),
  #path('borrar_dieta', views.borrar_dieta, name='borrar_dieta'),
  #path('editar_usuario', views.editar_usuario, name='editar_usuario'),
]

