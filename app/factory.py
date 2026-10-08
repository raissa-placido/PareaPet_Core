from core.implementation.services.dao import CategoriaDAO_ORM, ConexaoBD_ORM, ProdutoDAO_ORM
from core.implementation.services.repository import CategoriaService, ProdutoService


class ServicosFactory:

    def obter_conexao_bd(self):
        return ConexaoBD_ORM()

    def obter_categoria_dao(self):
        return CategoriaDAO_ORM(self.obter_conexao_bd())
    
    def obter_produto_dao(self):
        return ProdutoDAO_ORM(self.obter_conexao_bd())

    def obter_categoria_service(self):
        return CategoriaService(self.obter_categoria_dao())

    def obter_produto_service(self):
        return ProdutoService(self.obter_produto_dao())
