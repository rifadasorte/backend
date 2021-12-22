from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING, SET_NULL
from django.db.models.signals import post_save
from threading import Timer

# Create your models here.

class Premio(models.Model):
    imagem = models.ImageField()
    nome = models.CharField(max_length=50)
    valor = models.FloatField()
    def __str__(self):
        return self.nome

class status_sorteio(models.Choices):
    aberto = 'ABERTO'
    fechado = 'FECHADO'

class Sorteio(models.Model):
    premio = models.OneToOneField(Premio, related_name='prize_draw', on_delete=models.CASCADE)
    quantidade_de_numeros = models.IntegerField()
    preco_da_rifa = models.FloatField()
    criado_em = models.DateField(auto_now_add=True)
    data_do_sorteio = models.DateField()
    vencedor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, choices=status_sorteio.choices, default=status_sorteio.aberto)

    def __str__(self):
        return self.premio.nome

class status_requisicao(models.Choices):
    aberto = 'ABERTO'
    fechado = 'FECHADO'
    cancelado = 'CANCELADO'

class Requisicao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=status_requisicao.choices, default=status_requisicao.aberto)
    criado_em = models.DateField(auto_now_add=True)
    data_pagamento = models.DateField(null=True, blank=True)
    codigo_de_transacao = models.CharField(max_length=255)

class status(models.Choices):
    livre = 'LIVRE'
    reservado = 'RESERVADO'
    vendido = 'VENDIDO'

class Numeros(models.Model):
    codigo = models.CharField(max_length=4)
    proprietario = models.ForeignKey(
                        User, 
                        on_delete=models.SET_NULL, 
                        null=True,
                        blank=True)
    requisicao = models.ForeignKey(
                        Requisicao, 
                        on_delete=SET_NULL, 
                        related_name='req_num', 
                        null=True, 
                        blank=True)
    status = models.CharField(max_length=50, choices=status.choices, default=status.livre)
    sorteio = models.ForeignKey(Sorteio, on_delete=models.CASCADE, related_name='numbers_draw')

    def __str__(self):
        return self.codigo

class Telefone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    numero = models.CharField(max_length=15)

def generate_numbers(numbers):
    array_number = []
    digits = len(str(numbers-1))
    for num in range(numbers):
        array_number.append(((digits - len(str(num)))*'0') + str(num))
    return array_number

def post_save_draw(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']
    if(created):
        nums = generate_numbers(instance.quantidade_de_numeros)
        for code in nums:
            number = Numeros.objects.create(
                codigo = code,
                sorteio = instance
            ) 
            number.save()

def check_if_paid(request):
    if(request.status == status_requisicao.aberto):
        request.status = status_requisicao.cancelado
        request.save()

def post_save_request(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']
    if(created):
        interval = 60
        timer = Timer(interval, check_if_paid, args=(instance,))
        print('gerou timer', timer)
        timer.start()
    elif(instance.status == status_requisicao.fechado):
        for num in Numeros.objects.filter(requisicao=instance):
            num.status = status.vendido
            num.save()
    elif(instance.status == status_requisicao.cancelado):
        for num in Numeros.objects.filter(requisicao=instance):
            num.status = status.livre
            num.requisicao = None
            num.proprietario = None
            num.save()

post_save.connect(post_save_draw, sender=Sorteio)
post_save.connect(post_save_request, sender=Requisicao)