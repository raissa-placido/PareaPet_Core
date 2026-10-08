import sys

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.factory import ServicosFactory
from app.forms import CategoriaForm, ProdutoForm
from core.domain.entities.dominio import Categoria, Produto


# Método responsavel por listar, incluir, alterar e excluir as Categorias.
def categorias(request, acao=None, id=None):
    try:
        # define a classe de serviço
        servico = ServicosFactory().obter_categoria_service()

        # Listar registros
        # 'categorias/': Exibir a pagina de listagem
        if acao is None:
            # obtem os registros usando o serviço
            registros = servico.listar()
            return render(request, 'categorias_listar.html', context={'registros': registros})
        
        # Salvar registro
        # 'categorias/salvar/': insere, altera ou exclui um registro
        elif acao == 'salvar':
            form_data = request.POST
            acao_form = form_data['acao']

            try:
                if acao_form == 'Inclusão':
                    categoria = Categoria(descricao=form_data['descricao'])
                    # inclui a categoria usando o serviço
                    servico.incluir(categoria)

                elif acao_form == 'Exclusão':
                    id = int(form_data['id'])
                    # exclui a categoria usando o serviço
                    servico.excluir(id)

                else:
                    categoria = Categoria(
                        id=int(form_data['id']), 
                        descricao=form_data['descricao']
                    )
                    # altera a categoria usando o serviço
                    servico.alterar(categoria)

                # Sempre retornar um HttpResponseRedirect após processar dados "POST". 
                # Isso evita que os dados sejam postados 2 vezes caso usuário clicar "Voltar".
                return HttpResponseRedirect( reverse("categorias") )

            # se ocorreu algum erro, insere a mensagem para ser exibida no contexto da página 
            except Exception as err:
                return render(request, 'categorias_editar.html', 
                              context={
                                    'acao': acao_form, 
                                    'form': CategoriaForm(data=form_data),
                                    'ERRO': err,
                                })
        
        # inserir registro
        # 'categorias/incluir/': Exibir a pagina de inclusão
        elif acao == 'incluir':
            return render(request, 'categorias_editar.html',
                           context={'acao': 'Inclusão', 'form': CategoriaForm() })
        
        # Alterar ou excluir registro
        # 'categorias/alterar/<:id>/': Exibir a pagina de alteração
        # 'categorias/excluir/<:id>/': Exibir a pagina de exclusão
        elif acao in ['alterar', 'excluir']:
            acao = 'Alteração' if acao == 'alterar' else 'Exclusão'

            # seleciona o registro pelo id informado
            categoria = servico.obter_por_id(id)
            form = CategoriaForm({'id': categoria.id, 'descricao': categoria.descricao})

            return render(request, 'categorias_editar.html', 
                           context={'acao': acao, 'form': form })
        
        # acao INVALIDA
        else:
            raise Exception('Ação inválida')

    # se ocorreu algum erro, insere a mensagem para ser exibida no contexto da página 
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})




# Método responsavel por listar, incluir, alterar e excluir os Produtos.
def produtos(request, acao=None, id=None):
    try:
        # define a classe de serviço
        servico = ServicosFactory().obter_produto_service()

        # Listar registros
        # 'produtos/': Exibir a pagina de listagem
        if acao is None:
            # obtem os registros usando o serviço
            registros = servico.listar()
            return render(request, 'produtos_listar.html', context={'registros': registros})
        
        # Salvar registro
        # 'produtos/salvar/': insere, altera ou exclui um registro
        elif acao == 'salvar':
            form_data = request.POST
            acao_form = form_data['acao']

            try:
                if acao_form == 'Inclusão':
                    # converte os dados do formulario para objeto 
                    produto = Produto(
                            id=None, 
                            descricao=form_data['descricao'],
                            preco_unitario=float(form_data['preco_unitario']),
                            quantidade_estoque=int(form_data['quantidade_estoque']),
                            categoria=Categoria(
                                id=int(form_data['categoria_id']), 
                                descricao=None,
                            ),
                    ) 
                    # inclui o produto usando o serviço
                    servico.incluir(produto)

                elif acao_form == 'Exclusão':
                    id = int(form_data['id'])
                    # exclui o produto usando o serviço
                    servico.excluir(id)

                else:
                    # converte os dados do formulario para objeto 
                    produto = Produto(
                            id=int(form_data['id']), 
                            descricao=form_data['descricao'],
                            preco_unitario=float(form_data['preco_unitario']),
                            quantidade_estoque=int(form_data['quantidade_estoque']),
                            categoria=Categoria(
                                id=int(form_data['categoria_id']), 
                                descricao=None,
                            ),
                    ) 
                    # altera o produto usando o serviço
                    servico.alterar(produto)


                # Sempre retornar um HttpResponseRedirect após processar dados "POST". 
                # Isso evita que os dados sejam postados 2 vezes caso usuário clicar "Voltar".
                return HttpResponseRedirect( reverse("produtos") )
            
            # se ocorreu algum erro, insere a mensagem para ser exibida no contexto da página 
            except Exception as err:
                return render(request, 'produtos_editar.html', 
                              context={
                                    'acao': acao_form, 
                                    'form': ProdutoForm(data=form_data),
                                    'ERRO': err,
                                })
        
        # inserir registro
        # 'produtos/incluir/': Exibir a pagina de inclusão
        elif acao == 'incluir':
            return render(request, 'produtos_editar.html',
                           context={'acao': 'Inclusão', 'form': ProdutoForm() })
        
        # Alterar ou excluir registro
        # 'produtos/alterar/<:id>/': Exibir a pagina de alteração
        # 'produtos/excluir/<:id>/': Exibir a pagina de exclusão
        elif acao in ['alterar', 'excluir']:
            acao = 'Alteração' if acao == 'alterar' else 'Exclusão'

            # seleciona o registro pelo id informado
            produto = servico.obter_por_id(id)
            form = ProdutoForm({
                'id': produto.id, 
                'descricao': produto.descricao,
                'preco_unitario': produto.preco_unitario,
                'quantidade_estoque': produto.quantidade_estoque,
                'categoria_id': produto.categoria.id,
                'categoria': produto.categoria.descricao,
            })

            return render(request, 'produtos_editar.html', 
                           context={'acao': acao, 'form': form })
        
        # acao INVALIDA
        else:
            raise Exception('Ação inválida')

    # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
    except Exception as err:
        raise Exception(f'Erro ao processar a requisição: {err}') from err
        # return render(request, 'home.html', context={'ERRO': err})


# Exibe a página inicial da aplicação
def home(request):
    '''Exibe a pagina inicial da aplicação'''
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)


