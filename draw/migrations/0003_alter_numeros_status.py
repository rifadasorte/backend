# Generated by Django 4.0 on 2021-12-21 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0002_alter_numeros_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numeros',
            name='status',
            field=models.CharField(choices=[('LIVRE', 'Livre'), ('RESERVADO', 'Reservado'), ('VENDIDO', 'Vendido')], default='LIVRE', max_length=50),
        ),
    ]
