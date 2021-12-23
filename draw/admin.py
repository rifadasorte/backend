from django.contrib import admin
from .models import (Numeros, Premio, Requisicao, Sorteio, Telefone)

class NumberInline(admin.StackedInline):
    model = Numeros

class DrawAdmin(admin.ModelAdmin):
    list_display = ('premio', 
                    'quantidade_de_numeros', 
                    'preco_da_rifa',
                    'tempo_de_reserva',
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
