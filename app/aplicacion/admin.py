from django.contrib import admin
from .models import Producto, Usuario, Dieta

class UsuarioAdmin(admin.ModelAdmin):
      list_display    = ['usuario', 'email','contraseña', 'nombre', 'apellidos','fecha_nacimiento','genero','altura', 'peso', 'imagen', 'administrador','activo','created_on','updated_on']

class ProductoAdmin(admin.ModelAdmin):
      list_display    = ['nombre','marca','tienda','pais','alergenos','cantidad_servicio','aditivos','puntuacion_nova','image_url','image_small_url','calorias','energia','grasa','grasas_saturadas','grasas_trans','colesterol','carbohidratos','azucares','fibra','proteinas','sal','sodio','calcio','hierro','puntuacion']

class DietaAdmin(admin.ModelAdmin):
      list_display    = ['nombre', 'descripcion','usuario']

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Dieta, DietaAdmin)