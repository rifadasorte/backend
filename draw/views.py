from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Numeros, Sorteio, Telefone, Requisicao, check_if_paid
from .serializers import NumbersSerializer, DrawsSerializer
# Create your views here.

class GetNumbers(APIView):
    def get(self, request, pk):
        numbers = Numeros.objects.filter(sorteio__id = pk).order_by('-codigo')
        serializer = NumbersSerializer(numbers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetDraws(APIView):
    def get(self, request):
        draws = Sorteio.objects.all()
        serializer = DrawsSerializer(draws, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Authentication(APIView):
    def post(self, request):
        data = request.data
        try:
            username = data['username']
            email = data['email']
            num_tel = data['phone']
            password = data['password']
            user = User.objects.create_user(username = username,
                        email = email,
                        password = password)
            user.save()
            phone = Telefone.objects.create(user = user, numero = num_tel)
            phone.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

def check_if_free(numeros):
    for num in numeros:
        num = Numeros.objects.get(codigo=num['codigo'])
        if(num.status == 'RESERVADO' or num.status == ['VENDIDO']):
            return False
    return True

class SetRequest(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        if(not check_if_free(data)):
            return Response(
                data={"error":"você selecionou números reservados"}, 
                status=status.HTTP_400_BAD_REQUEST)
    #try:
        _request = Requisicao.objects.create(user=user, codigo_de_transacao='9090')
        _request.save()
        for num in data:
            numero = Numeros.objects.get(codigo=num['codigo'])
            numero.proprietario = user
            numero.requisicao = _request
            numero.status = 'RESERVADO'
            numero.save()
        return Response(status=status.HTTP_200_OK)
    #except:
    #    return Response(data={"error":"Algo deu errado"}, status=status.HTTP_400_BAD_REQUEST)


