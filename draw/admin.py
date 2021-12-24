from django.contrib import admin
from .models import (Numeros, Premio, Requisicao, Sorteio, Telefone)
from django_admin_inline_paginator.admin import TabularInlinePaginated

class NumberInline(TabularInlinePaginated):
    model = Numeros
    per_page = 100

class DrawAdmin(admin.ModelAdmin):
    list_display = ('premio', 
                    'quantidade_de_numeros', 
                    'preco_da_rifa',
                    'criado_em',
                    'data_do_sorteio',
                    'vencedor')
    inlines = [
                NumberInline,
    ]

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 
                    'status',
                    'criado_em',
                    'data_pagamento',
                    'codigo_de_transacao')
    inlines = [
        NumberInline,
    ]

class TelefoneAdmin(admin.ModelAdmin):
    list_display = ('user', 'numero',)
    search_fields = ('user',)

admin.site.register(Sorteio, DrawAdmin)
admin.site.register(Premio)
admin.site.register(Telefone, TelefoneAdmin)
admin.site.register(Requisicao, RequestAdmin)
