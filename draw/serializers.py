from rest_framework.serializers import ModelSerializer
from .models import Numeros

class NumbersSerializer(ModelSerializer):
    class Meta:
        model = Numeros
        fields = ['codigo', 'proprietario', 'status']