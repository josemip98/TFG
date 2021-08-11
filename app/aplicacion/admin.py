from django.contrib import admin
from .models import Producto, Usuario, Dieta

class UsuarioAdmin(admin.ModelAdmin):
      list_display    = ['usuario', 'email','password', 'nombre', 'apellidos','fecha_nacimiento','genero','altura', 'peso', 'imagen', 'administrador','activo','created_on','updated_on']

class ProductoAdmin(admin.ModelAdmin):
      list_display    = ['nombre','marca','tienda','pais','alergenos','aditivos','puntuacion_nova','image_url','calorias','energia','grasa','grasas_saturadas','colesterol','carbohidratos','azucares','fibra','proteinas','sal','sodio','calcio','hierro','puntuacion']

class DietaAdmin(admin.ModelAdmin):
      list_display    = ['nombre', 'descripcion','get_productos','usuario']


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Dieta, DietaAdmin)