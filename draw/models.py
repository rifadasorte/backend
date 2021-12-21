from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING
from django.db.models.signals import post_save

# Create your models here.

class Premio(models.Model):
    imagem = models.ImageField()
    nome = models.CharField(max_length=50)
    valor = models.FloatField()
    def __str__(self):
        return self.nome

class Sorteio(models.Model):
    premio = models.OneToOneField(Premio, related_name='prize_draw', on_delete=models.CASCADE)
    quantidade_de_numeros = models.IntegerField()
    preco_da_rifa = models.FloatField()
    criado_em = models.DateField(auto_now_add=True)
    data_do_sorteio = models.DateField()
    vencedor = models.ForeignKey(User, null=True, blank=True, on_delete=DO_NOTHING)

    def __str__(self):
        return self.premio.nome

class status(models.Choices):
    livre = 'LIVRE'
    reservado = 'RESERVADO'
    vendido = 'VENDIDO'

class Numeros(models.Model):
    codigo = models.CharField(max_length=4)
    proprietario = models.ForeignKey(User, 
            on_delete=models.PROTECT, 
            related_name='user_numbers',
            null=True,
            blank=True)
    status = models.CharField(max_length=50, choices=status.choices, default=status.livre)
    sorteio = models.ForeignKey(Sorteio, on_delete=models.CASCADE, related_name='numbers_draw')
    def __str__(self):
        return self.codigo

class status_requisicao(models.Choices):
    aberto = 'ABERTO'
    fechado = 'FECHADO'
    cancelado = 'CANCELADO'

class Requisiçao(models.Model):
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    numeros = models.ManyToManyField(Numeros,related_name='red_num')
    status = models.CharField(max_length=50, choices=status_requisicao.choices, default=status_requisicao.aberto)
    codigo_de_trasacao = models.CharField(max_length=255)

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

def post_save_requisicao(sender, **kwargs):
    instance = kwargs['instance']
    if(instance.status == status_requisicao.aberto):
        for num in instance.numeros:
            num.status = status.reservado
    elif(instance.status == status_requisicao.fechado):
        for num in instance.numeros:
            num.status = status.vendido
    elif(instance.status == status_requisicao.cancelado):
        for num in instance.numeros:
            num.status = status.livre

post_save.connect(post_save_draw, sender=Sorteio)
post_save.connect(post_save_requisicao, sender=Requisiçao)