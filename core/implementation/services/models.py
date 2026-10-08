from django.db import models
from django.utils import timezone
import datetime


# Define o Model de Categoria
class CategoriaModel(models.Model):
    # define os campos
    id = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=30)

    class Meta:
        # define o nome da tabela
        db_table = 'Categoria'


# Define o Model de Produto
class ProdutoModel(models.Model):
    # define os campos
    id = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=30)
    preco_unitario = models.FloatField()
    quantidade_estoque = models.IntegerField()
    categoria = models.ForeignKey(CategoriaModel, on_delete=models.RESTRICT)

    class Meta:
        # define o nome da tabela
        db_table = 'Produto'

