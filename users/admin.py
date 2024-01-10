from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from lista_desejos.admin import ListaDesejosInline

class CustomUserAdmin(UserAdmin):
    inlines = (ListaDesejosInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
