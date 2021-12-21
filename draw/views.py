from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Numeros
from .serializers import NumbersSerializer
# Create your views here.

class GetNumbers(APIView):
    def get(self, request, pk):
        numbers = Numeros.objects.filter(sorteio__id = pk)
        serializer = NumbersSerializer(numbers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


