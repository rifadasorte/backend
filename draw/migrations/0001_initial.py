# Generated by Django 4.0 on 2021-12-21 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Premio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='')),
                ('nome', models.CharField(max_length=50)),
                ('valor', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Sorteio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_de_numeros', models.IntegerField()),
                ('preco_da_rifa', models.FloatField()),
                ('criado_em', models.DateField(auto_now_add=True)),
                ('data_do_sorteio', models.DateField()),
                ('premio', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='prize_draw', to='draw.premio')),
                ('vencedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Numeros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=4)),
                ('status', models.CharField(choices=[('LIVRE', 'Livre'), ('RESERVADO', 'Reservado'), ('VENDIDO', 'Vendido')], default='LIVRE', max_length=50)),
                ('proprietario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_numbers', to='auth.user')),
                ('sorteio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numbers_draw', to='draw.sorteio')),
            ],
        ),
    ]
