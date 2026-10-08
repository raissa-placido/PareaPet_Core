from abc import ABC, abstractmethod
from typing import Any

from core.domain.entities.dominio import Categoria, Produto
from core.domain.services.interfaces_dao import ICategoriaDAO, IConexaoBD, IProdutoDAO

from django.db import connections
from django.forms.models import model_to_dict

from dataclasses import asdict

from core.implementation.services.models import CategoriaModel, ProdutoModel


class ConexaoBD_ORM(IConexaoBD):
    
    # nome usado para identificar a conexao com o BD no Django
    DB_ALIAS = 'db_solid'

    def obter_conexao(self):
        '''Estabelece a conexao com o SQLite usando o ORM do Django'''

        # adiciona a configuração do BD na configuração do Django
        # Obs: adiciona apenas se ainda não tiver sido adicionada
        if self.DB_ALIAS not in connections.databases:
            connections.databases[self.DB_ALIAS] = {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': 'db_solid.sqlite3',
                    'ATOMIC_REQUESTS': False,  
                    'TIME_ZONE': 'America/Fortaleza',
                    "CONN_HEALTH_CHECKS": True,
                    "CONN_MAX_AGE": 60,  
                    'AUTOCOMMIT': True,
                    "OPTIONS": {
                    },
            }    

        # retorna a conexao com o BD
        return connections[self.DB_ALIAS]

    def executar_comando(self, sql_comando, commit=True) -> Any:
        '''Executa um comando SQL no BD (geralmente um INSERT, UPDATE ou DELETE)'''
        # obtem conexao
        conexao = self.obter_conexao()
        # cria um cursor() e executa o SQL informado
        ret = conexao.cursor().execute(sql_comando)
        
        # ======================================================
        # OBS: NÃO PRECISA FAZER O COMMIT MANUALMENTE POR   
        #      CAUSA DA CONFIGURAÇÃO ['AUTOCOMMIT': True]
        # ======================================================
        # verifica se eh para efetivar as modificações no BD
        # if commit:
        #     conexao.commit()
        
        # retorna o resultado da execução do comando SQL
        return ret 

    def executar_select(self, sql_select) -> list[Any]:
        '''Executa um comando SELECT no BD e retorna os registros'''
        # obtem conexao
        conexao = self.obter_conexao()
        # cria um cursor(), executa o SELECT informado e traz os todos os registros
        ret = conexao.cursor().execute(sql_select).fetchall()
        # retorna os registros do BD
        return ret 



class CategoriaDAO_ORM(ICategoriaDAO):

    def __init__(self, conexao: IConexaoBD): 
        self._conexao = conexao
        # chama o método obter_conexao() para garantir que 
        # a configuração do BD seja adicionada no Django
        self._conexao.obter_conexao()

    def incluir(self, obj: Categoria) -> Categoria: 
        # Cria instancia do model a partir da classe de dominio
        model_instance = CategoriaModel( **asdict(obj) )
        # inclui registro usando ORM
        model_instance.save( using=self._conexao.DB_ALIAS )
        # retorna o objeto de dominio com o id gerado pelo BD
        return Categoria( **model_to_dict(model_instance) )

    def alterar(self, obj: Categoria) -> Categoria: 
        # reaproveita o método incluir para fazer a alteração, 
        # pois o ORM do Django entende que se o ID do objeto já existe, 
        # ele deve ser atualizado ao invés de inserido
        return self.incluir(obj)
    
    def excluir(self, id: int): 
        # Cria instancia do model a partir do ID informado
        model_instance = CategoriaModel(id=id)
        # exclui registro usando ORM
        model_instance.delete( using=self._conexao.DB_ALIAS )
    
    def obter_por_id(self, id: int) -> Categoria: 
        # obtem todos os registros usando ORM
        registro = CategoriaModel.objects.using(self._conexao.DB_ALIAS).get(id=id)
        # converte o registro em classe de domínio e retorna
        return Categoria( **model_to_dict(registro) )
    
    def listar(self) -> list[Categoria]: 
        # obtem todos os registros usando ORM
        registros = CategoriaModel.objects.using(self._conexao.DB_ALIAS).all().order_by('descricao')
        # converte os registros para classes de dominio e adiciona na lista
        dados = [Categoria( **model_to_dict(registro) ) for registro in registros]
        # retorna
        return dados    




class ProdutoDAO_ORM(IProdutoDAO):

    def __init__(self, conexao: IConexaoBD): 
        self._conexao = conexao
        # chama o método obter_conexao() para garantir que 
        # a configuração do BD seja adicionada no Django
        self._conexao.obter_conexao()

    def incluir(self, obj: Produto) -> Produto: 
        # converte o objeto de dominio para dicionário, 
        # removendo a chave 'categoria' (Foreign Key) para evitar problemas
        # na criação do model instance
        obj_asdict = asdict(obj)
        obj_asdict.pop('categoria')

        # Cria instancia do model a partir da classe de dominio
        model_instance = ProdutoModel( **obj_asdict )
        # atribui a categoria_id (Foreign Key) usando o 
        # id da categoria do objeto de dominio
        model_instance.categoria_id = obj.categoria.id

        # inclui registro usando ORM
        model_instance.save( using=self._conexao.DB_ALIAS )
        # retorna o objeto de dominio com o id gerado pelo BD
        return Produto( **model_to_dict(model_instance) )

    def alterar(self, obj: Produto) -> Produto: 
        # reaproveita o método incluir para fazer a alteração, 
        # pois o ORM do Django entende que se o ID do objeto já existe, 
        # ele deve ser atualizado ao invés de inserido
        return self.incluir(obj)
    
    def excluir(self, id: int): 
        # Cria instancia do model a partir do ID informado
        model_instance = ProdutoModel(id=id)
        # exclui registro usando ORM
        model_instance.delete( using=self._conexao.DB_ALIAS )


    def helper_converter_model_para_dominio(self, model_instance):
        # converte o registro em dicionário para criar o objeto de domínio
        produto_dict = model_to_dict(model_instance)

        # remove a chave 'categoria' do dicionário para 
        # evitar problemas na criação do objeto de domínio
        produto_dict.pop('categoria') 

        # cria o objeto de domínio a partir do dicionário do Model
        produto = Produto( **produto_dict )

        # Adiciona a categoria (Foreign Key) usando o Model
        produto.categoria = Categoria( **model_to_dict(model_instance.categoria) )

        # retorna o objeto de domínio        
        return produto


    def obter_por_id(self, id: int) -> Produto: 
        # obtem todos os registros usando ORM
        registro = ProdutoModel.objects.using(self._conexao.DB_ALIAS).get(id=id)
        # converte o registro em classe de domínio e retorna
        return self.helper_converter_model_para_dominio(registro) 
    

    def listar(self) -> list[Produto]: 
        # obtem todos os registros usando ORM
        registros = ProdutoModel.objects. \
                    using(self._conexao.DB_ALIAS). \
                    select_related('categoria'). \
                    all().order_by('descricao')

        # converte os registros para classes de dominio e adiciona na lista
        dados = [
            self.helper_converter_model_para_dominio(registro) 
            for registro in registros
        ]
        # retorna
        return dados    
