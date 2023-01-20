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