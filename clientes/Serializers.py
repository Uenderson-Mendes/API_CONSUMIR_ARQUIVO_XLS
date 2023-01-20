from rest_framework import serializers
from clientes.models import Dados_existentes







class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dados_existentes
        fields = '__all__'
        