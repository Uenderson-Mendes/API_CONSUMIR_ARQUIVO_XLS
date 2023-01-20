# API_CONSUMIR_ARQUIVO_XlSX 📁
# criando API_consumir arquivo xlsx

Para criação da API iniciamos criando uma pasta com o nome da referência a aplicação. Lembrando que utilizaremos o ambiente virtual para criação do projeto

## 1ª vamos criar uma pasta e ascessa-lá pelo VSCODE
logo após criar e ascessar a pasta criada vamos dar inicio a criação do nosso projeto...

### ⚠️Atenção demonstração do projeto no final do tutorial!!!

## Criando ambiente virtual

Criando  ambiente virtual 

Windows
```bash
python3 -m venv env 
```
Linux
```bash
virtualenv env
```


comando para ativar ambiente virtual  windows

```bash
. env/Scripts/activate
```
comando para ativar ambiente virtual  no Linux

```bash
. env/bin/activate
```

Caso queira desativar o ambiente virtual,

```bash
deactivate
```

## instalações nescessarias 
 1ª 
 ```bash
 pip install virtualenv
 pip install pandas
 pip install openpyxl  
 ```
2ª Instalando frameworks
```bash
pip install django
pip install djangorestframework
pip install markdown       
pip install django-filter  # Filtering support
```
## Criando projeto e Aplicação

para criar o projeto use 
```bash
django-admin startproject core .
```


para criar sua aplicação use:
```bash
django-admin startapp consumir
```
## Configurando o settings.py
```bash

    INSTALLED_APPS = [
        ...
     'rest_framework',
      'clientes',
      'django_filters',
    ]
```
## Criando os modelos para nosso clientes
No arquivo clientes/models.py definimos todos os objetos chamados Modelos  que sera o nosso banco de dados:

```bash
from django.db import models



class Dados_existentes(models.Model):
    NIVEL = (
    ('F', 'F'),
    ('M', 'M'))

    nome = models.CharField('Nome Cadastrado:',max_length=100,null=True)
    sobrenome = models.CharField('Sobre Nome:',max_length=150, blank=True,null=True)
    sexo = models.CharField(max_length=1, choices=NIVEL, blank=False, null=False, default='M')
    altura = models.CharField(max_length=20,null=True)
    peso = models.CharField(max_length=20,null=True)
    nascimento= models.DateField(null=True)
    bairro = models.CharField(max_length=150,null=True)
    cidade = models.CharField(max_length=200,null=True)
    estado = models.CharField(max_length=200,null=True)
    numero = models.CharField('nome',max_length=30,null=True)

    def __str__(self):
        return self.nome
    objects = models.Manager()
```
Logo após Aplique os seguinte comandos:
```bash
python manage.py makemigrations clientes
python manage.py migrate clientes
python manage.py migrate 
```
## Criando administrador ou Django Admin
adicione nome, e-mail, e senha
```bash
python manage.py createsuperuser
```
## arquivo admin.py
Vamos abrir clientes/admin.py no editor de código, apagar tudo dele e escrever o seguinte código:

```
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


```

## arquivo Serializers.py
Vamos abrir clientes/Serializers.py no editor de código, apagar tudo dele e escrever o seguinte código:
```bash
from rest_framework import serializers
from clientes.models import Dados_existentes


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dados_existentes
        fields = '__all__'
```
## arquivo views.py
Vamos abrir clientes/views.py no editor de código, apagar tudo dele e escrever o seguinte código:

```bash
from .Serializers import ClienteSerializer
from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework import viewsets
from clientes.models import  Dados_existentes
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
import pandas as pd
from http.client import HTTPResponse
from django.shortcuts import render
import pandas as pd
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime


 
class ClientesViewSet(viewsets.ModelViewSet):
    """Listando clientes"""
    queryset = Dados_existentes.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['nascimento'] #ordenar por nome
    filterset_fields = ['sexo','cidade']
# Create your views here
class FiltroViewSet(viewsets.ModelViewSet):
    """Listando clientes"""
    queryset = Dados_existentes.objects.filter(cidade='Meeren',sexo='F')
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['nascimento'] #ordenar por nome
  

def cadastro(request):
        
        if request.method == 'POST' and request.FILES['myfile']:      
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename) 
            cwd = os.getcwd()             
            empexceldata = pd.read_excel(f'{cwd}/media_root/{myfile}',engine="openpyxl")        
            dbframe = empexceldata
        
            for dbframe in dbframe.itertuples():
                obj = Dados_existentes.objects.create( id=dbframe.id,nome=dbframe.nome,
                                                 sobrenome=dbframe.sobrenome,   sexo=dbframe.sexo, altura=dbframe.altura, peso=dbframe.peso,
                                                nascimento=datetime.fromtimestamp(dbframe.nascimento),  bairro=dbframe.bairro,cidade=dbframe.cidade,estado=dbframe.estado,numero=dbframe.numero)           
            obj.save()
            return render(request, 'index.html', {
                'uploaded_file_url': uploaded_file_url
            })
         
        return render(request,'index.html',{})
        
      

```
## core/urls.py
Vamos abrir core/urls.py no editor de código, apagar tudo dele e escrever o seguinte código:

```bash
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from clientes.views import ClientesViewSet
from clientes import views

router = routers.DefaultRouter()
router.register('Dados_Clientes', ClientesViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clientes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
## clientes/urls.py
Vamos abrir clientes/urls.py no editor de código, apagar tudo dele e escrever o seguinte código:

```bash
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from clientes.views import ClientesViewSet, FiltroViewSet
from clientes import views

router = routers.DefaultRouter()
router.register('Dados_Clientes_Geral', ClientesViewSet,'dados clientes')
router.register('mulheres_de_Meeren', FiltroViewSet,'mulheres')



urlpatterns = [
    path('', views.cadastro, name='cadastro'),
    path('cadastr',include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
## criando formulario de upload
crie um pasta clientes/templates/index.html:

```bash
{% load static %}

{% block content %}

<!DOCTYPE html>
<html lang="en">
  <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
  <link rel="stylesheet" href="{% static 'navbar-top-fixed.css' %}">
  <link rel="stylesheet" href="{% static 'https://fonts.googleapis.com/css?family=Heebo:400,700|Oxygen:700' %}"> 
  <link rel="stylesheet" href="{% static 'dist/css/style.css' %}">

  <nav class="navbar navbar-expand-lg bg-body-tertiary btn-success">
    <div class="container-fluid">
      
      <a class="btn btn-success " href="http://127.0.0.1:8000/cadastr">API</a></button
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
      
      </div>
    </div>
  </nav>

 <center>
  <form method="POST" enctype="multipart/form-data" class=".bg-success-subtle">
    
    {% csrf_token %} 
<div class="card " style="width: 25rem;">
  <img src="https://cdnsjengenhariae.nuneshost.com/wp-content/uploads/2018/02/excel-formulas-1.jpg"  class="card-img-top" alt="...">
  <div class="card-body ">
    <h5 class="card-title">Faça o Upload do arquivo</h5>
   
  </div>
  <ul class="list-group list-group-flush">
    <li class="list-group-item">     <input type="file" name="myfile" class="form-control"required></li>
  </ul>
  <div class="card-body">
    <a href="#" class="card-link"> <button type="submit" class="btn btn-dark" required>Upload</button> </a>
  </div>
</div>
  </form>  


</center> 
{% endblock %}

```
#instale o framework de estilização Boostrap: 

[Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/download/)

### logo após isso configure os arquivos staticos 

crie uma pasta da seguinte forma: clientes/static armazene seu css, javascript e bootstrap nela
logo apos vá ate o arquivo core/settings.py e adicione o seguinte codigos
```bash 
TEMPLATES = [
    {
        .....
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
 ```
 e os campos:
 ```bash
  STATIC_URL = 'static/'
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')
  MEDIA_URL = '/media/'
```

adicione tambem no mesmo arquivo settings.py no final do arquivo o seguinte:
```bash
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'] #novo
}
```
# Testando
Vamos startar o servidor web
```bash
python manage.py runserver 
```
```bash
http://127.0.0.1:8000/
```
## Documentação de apoio:
[Django REST framework](https://www.django-rest-framework.org/)

[Django](https://docs.djangoproject.com/pt-br/4.1/)

[Pandas](https://pandas.pydata.org/docs/user_guide/index.html#user-guide)


# Assista ao video de demostração

## [🎬Demontração](https://drive.google.com/file/d/1oTdjCNRtDAkl-THZz7g4nWAEMfn2uNon/view)

# congratulations 😎
![exemplo](https://gifburg.com/images/gifs/congratulations/gifs/0006.gif)  👉🏼👉🏼👉🏼    ![e](https://media.tenor.com/MXnkudfpfSUAAAAM/yeah-woohoo.gif)

