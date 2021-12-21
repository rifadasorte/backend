from django.contrib import admin
from .models import Numeros, Premio, Sorteio

class NumberInline(admin.TabularInline):
    model = Numeros

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

admin.site.register(Sorteio, DrawAdmin)
admin.site.register(Premio)