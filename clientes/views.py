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
        
      

     





