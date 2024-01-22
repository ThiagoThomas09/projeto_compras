from django.contrib import admin
from . models import *

class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 0

class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['user', 'criado_em', 'status_aberto']
    list_filter = ['status_aberto', 'criado_em']
    inlines = [ItemCarrinhoInline]

admin.site.register(Loja)
admin.site.register(Produto)
admin.site.register(Carrinho, CarrinhoAdmin)


