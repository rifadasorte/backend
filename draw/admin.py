from django.contrib import admin
from .models import (Numeros, Premio, Requisicao, Sorteio, Telefone)
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import EmptyPage, InvalidPage, Paginator

class InlineChangeList(object):
    can_show_all = True
    multi_page = True
    get_query_string = ChangeList.__dict__['get_query_string']

    def __init__(self, request, page_num, paginator):
        self.show_all = 'all' in request.GET
        self.page_num = page_num
        self.paginator = paginator
        self.result_count = paginator.count
        self.params = dict(request.GET.items())


class PaginationInline(admin.TabularInline):
    template = 'tabular_paginated.html'
    per_page = 20

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(PaginationInline, self).get_formset(
            request, obj, **kwargs)
        class PaginationFormSet(formset_class):
            def __init__(self, *args, **kwargs):
                super(PaginationFormSet, self).__init__(*args, **kwargs)

                qs = self.queryset
                paginator = Paginator(qs, self.per_page)
                try:
                    page_num = int(request.GET.get('p', '0'))
                except ValueError:
                    page_num = 0

                try:
                    page = paginator.page(page_num + 1)
                except (EmptyPage, InvalidPage):
                    page = paginator.page(paginator.num_pages)

                self.cl = InlineChangeList(request, page_num, paginator)
                self.paginator = paginator

                if self.cl.show_all:
                    self._queryset = qs
                else:
                    self._queryset = page.object_list

        PaginationFormSet.per_page = self.per_page
        return PaginationFormSet

class NumberInline(PaginationInline):
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
