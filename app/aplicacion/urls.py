from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^registro/$', views.registro, name='registro'),
  url(r'login/$', views.login, name='login'),
  url(r'^logout/$', views.logout_view, name='logout'),
  url(r'^lista_productos/$', views.lista_productos, name='lista_productos'),
  url(r'^producto/(?P<pk>\d+)$', views.productos_detalle, name='productos_detalle'),
  url(r'^aniadir_producto/$', views.aniadir_producto, name='aniadir_producto'),
  url(r'^modificar_producto/(?P<id_producto>\d+)$', views.modificar_producto, name='modificar_producto'),
  url(r'^borrar_producto/(?P<id_producto>\d+)$', views.borrar_producto, name='borrar_producto'),
  url(r'^buscar_producto/$', views.buscar_producto, name='buscar_producto'),
  url(r'^mostrar_perfil/$', views.mostrar_perfil, name='mostrar_perfil'),
  url(r'^modificar_perfil/(?P<id_usuario>\d+)$', views.modificar_perfil, name='modificar_perfil'),
  url(r'^borrar_perfil/$', views.borrar_perfil, name='borrar_perfil'),
  url('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
  url('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
  url('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  url('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
  url(r'^mostrar_dieta/$', views.mostrar_dieta, name='mostrar_dieta'),
  url(r'^mostrar_dieta/(?P<id_dieta>\d+)$', views.ver_dieta, name='ver_dieta'),
  url(r'^dieta/$', views.aniadir_dieta, name='aniadir_dieta'),
  url(r'^generar_dieta/$', views.generar_dieta, name='generar_dieta'),
  url(r'^contacto/$', views.contacto, name='contacto'),
  url('export/', views.export_pdf, name="export-pdf" )
  #url('modificar_dieta', views.modificar_dieta, name='modificar_dieta'),
  #url('borrar_dieta', views.borrar_dieta, name='borrar_dieta'),
]

