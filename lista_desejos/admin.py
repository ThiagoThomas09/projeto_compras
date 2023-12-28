from django.contrib import admin
from . models import *

class ItemListaDesejosInline(admin.TabularInline):
    model = ItemListaDesejos
    # define se vai ter campos vazios para adicionar novos itens
    extra = 0

class ListaDesejosAdmin(admin.ModelAdmin):
    inlines = [ItemListaDesejosInline]


admin.site.register(ListaDesejos, ListaDesejosAdmin)
