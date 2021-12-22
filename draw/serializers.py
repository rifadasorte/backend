from rest_framework.serializers import ModelSerializer
from .models import Numeros, Premio, Sorteio

class NumbersSerializer(ModelSerializer):
    class Meta:
        model = Numeros
        fields = ['codigo', 'proprietario', 'status']

class PrizeSerializer(ModelSerializer):
    class Meta:
        model = Premio
        fields = ['imagem', 'nome', 'valor']

class DrawsSerializer(ModelSerializer):
    premio = PrizeSerializer()
    class Meta:
        model = Sorteio
        fields = ['id',
                'premio', 
                'quantidade_de_numeros',
                'preco_da_rifa',
                'criado_em',
                'data_do_sorteio',
                'vencedor',
                'status']


