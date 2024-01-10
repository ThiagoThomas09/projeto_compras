from django.contrib import admin
from . models import *

class ListaDesejosInline(admin.TabularInline):
    model = ListaDesejos
    extra = 0
    fields = ('nome', 'criado_em')
    readonly_fields = ('nome', 'criado_em')

class ItemListaDesejosInline(admin.TabularInline):
    model = ItemListaDesejos
    # define se vai ter campos vazios para adicionar novos itens
    extra = 0

class ListaDesejosAdmin(admin.ModelAdmin):
    inlines = [ItemListaDesejosInline]
    list_display = ('nome', 'user', 'criado_em')


admin.site.register(ListaDesejos, ListaDesejosAdmin)
