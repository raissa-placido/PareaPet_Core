from abc import ABC, abstractmethod

from core.domain.entities.dominio import Categoria, Produto
from core.domain.services.interfaces_dao import ICategoriaDAO, IProdutoDAO
from core.domain.services.interfaces_repository import ICategoriaService


class CategoriaService(ICategoriaService):

    def __init__(self, dao: ICategoriaDAO ): 
        # define o DAO a ser utilizado pelo serviço
        self._dao = dao

    def validar(self, obj: Categoria): 
        # exemplo de regra de negócio: a descrição da categoria é obrigatória
        if (not obj.descricao) or (obj.descricao.strip() == ''):
            raise ValueError('A descrição da categoria é obrigatória.')

    def incluir(self, obj: Categoria) -> Categoria: 
        # valida o objeto de categoria        
        self.validar(obj)
        # delega a inclusão da categoria para o DAO
        obj = self._dao.incluir(obj)
        return obj

    def alterar(self, obj: Categoria) -> Categoria: 
        # valida o objeto de categoria        
        self.validar(obj)
        # delega a alteração da categoria para o DAO
        obj = self._dao.alterar(obj)
        return obj

    def excluir(self, id: int): 
        # delega a exclusão da categoria para o DAO
        self._dao.excluir(id)

    def obter_por_id(self, id: int): 
        # exemplo de regra de negócio: o id da categoria é obrigatório
        if not id:
            raise ValueError('O id da categoria deve ser informado.')
        # delega a obtenção da categoria para o DAO
        obj = self._dao.obter_por_id(id)
        return obj

    def listar(self) -> list[Categoria]: 
        # delega a listagem das categorias para o DAO
        return self._dao.listar()


class ProdutoService(ABC):

    def __init__(self, dao: IProdutoDAO ): 
        # define o DAO a ser utilizado pelo serviço
        self._dao = dao

    def validar(self, obj: Produto): 
        # a descrição do produto é obrigatória
        if (not obj.descricao) or (obj.descricao.strip() == ''):
            raise ValueError('A descrição do produto é obrigatória.')
        # o preço unitário deve ser maior que zero
        if (not obj.preco_unitario) or (obj.preco_unitario <= 0):
            raise ValueError('O preço unitário do produto deve ser maior que zero.')
        # a quantidade em estoque deve ser zero ou maior que zero
        if (obj.quantidade_estoque==None) or (obj.quantidade_estoque < 0):
            raise ValueError('A quantidade em estoque deve ser igual ou maior que zero.')
        # a categoria deve ser informada e deve ter um id válido
        if (not obj.categoria) or (obj.categoria.id==None) or (obj.categoria.id < 0):
            raise ValueError('A categoria do produto deve ser informada.')

    def incluir(self, obj: Produto) -> Produto: 
        # valida o objeto de produto        
        self.validar(obj)
        # delega a inclusão do produto para o DAO
        obj = self._dao.incluir(obj)
        return obj

    def alterar(self, obj: Produto) -> Produto: 
        # valida o objeto de produto        
        self.validar(obj)
        # delega a alteração do produto para o DAO
        obj = self._dao.alterar(obj)
        return obj

    def excluir(self, id: int): 
        # delega a exclusão do produto para o DAO
        self._dao.excluir(id)

    def obter_por_id(self, id: int): 
        # o id do produto é obrigatório
        if not id:
            raise ValueError('O id do produto deve ser informado.')
        # delega a obtenção do produto para o DAO
        obj = self._dao.obter_por_id(id)
        return obj

    def listar(self) -> list[Produto]: 
        # delega a listagem dos produtos para o DAO
        return self._dao.listar()
