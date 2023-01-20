from django.contrib import admin
from clientes.models import Dados_existentes

class dado(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('sexo',)
   
    list_per_page = 25
    ordering = ('nome',)



admin.site.register(Dados_existentes, dado)


