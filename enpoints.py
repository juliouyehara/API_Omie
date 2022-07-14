from omie import *
import pandas as pd
from config.catalog_config import CatalogConfig

config = CatalogConfig()
config.read()

class Endpoint:

    def request_conta_a_receber(api_omie):

        lista = []

        r = api_omie.request(config['OMIE_API']['URL_CATEGORIA'], call='ListarCategorias', params={
            "pagina": 1,
            "registros_por_pagina": 100
        }).json()
        for n in range(r['total_de_paginas']):
            r = api_omie.request(config['OMIE_API']['URL'],call='ListarContasReceber', params={
                  "pagina": n+1,
                  "registros_por_pagina": 40,
                  "apenas_importado_api": "N"
                }).json()
            print(r)
            for i in range(r['registros']):
                dict = {}
                codigo_categoria = (r['conta_receber_cadastro'][i]['categorias'][0]['codigo_categoria'])
                percentual = (r['conta_receber_cadastro'][i]['categorias'][0]['percentual'])
                valor = (r['conta_receber_cadastro'][i]['categorias'][0]['valor'])
                codigo_cliente = (r['conta_receber_cadastro'][i]['codigo_cliente_fornecedor'])
                codigo_omie = (r['conta_receber_cadastro'][i]['codigo_lancamento_omie'])
                data_emissao = (r['conta_receber_cadastro'][i]['data_emissao'])
                data_previsao = (r['conta_receber_cadastro'][i]['data_previsao'])
                numero_parcela = (r['conta_receber_cadastro'][i]['numero_parcela'])
                status_titulo = (r['conta_receber_cadastro'][i]['status_titulo'])
                tipo_agrupamento = (r['conta_receber_cadastro'][i]['tipo_agrupamento'])
                try:
                    codigo_vendedor = str((r['conta_receber_cadastro'][i]['codigo_vendedor']))
                    codigo_vendedor = str(codigo_vendedor)
                    codigo_vendedor = f'{codigo_vendedor}'
                except:
                    codigo_vendedor = ''
                dict.update({
                    'codigo categoria': codigo_categoria,
                    'percentual': percentual,
                    'valor': valor,
                    'codigo cliente': codigo_cliente,
                    'codigo omie': codigo_omie,
                    'data emissao': data_emissao,
                    'data previsao': data_previsao,
                    'numero parcela': numero_parcela,
                    'status titulo': status_titulo,
                    'tipo agrupamento': tipo_agrupamento,
                    'codigo vendedor': codigo_vendedor
                })
                lista.append(dict)

        df = pd.DataFrame(lista)
        df.to_csv('teste.csv')
        print(df)

    def request_vendedores(api_omie):

        lista = []
        r = api_omie.request(config['OMIE_API']['URL_VENDEDORES'],call='ListarVendedores', params={
          "pagina": 1,
          "registros_por_pagina": 40,
          "apenas_importado_api": "N"
        }).json()
        print(r)
        for i in range(r['total_de_registros']):
          dict = {}
          print(r['cadastro'][i])
          codigo_vendedor = (r['cadastro'][i]['codigo'])
          nome_vendedor = (r['cadastro'][i]['nome'])
          dict.update({'codigo vendedor': codigo_vendedor,
                       'nome vendedor': nome_vendedor
                       })
          lista.append(dict)
        return lista
        # df = pd.DataFrame(lista)
        # df.to_csv('teste_vendedores.csv')



    def request_clientes(api_omie):

        lista = []
        r = api_omie.request(config['OMIE_API']['URL_CLIENTES'], call='ListarClientes', params={
            "pagina": 1,
            "registros_por_pagina": 40,
            "apenas_importado_api": "N"
        }).json()
        for n in range(r['total_de_paginas']):

            r = api_omie.request(config['OMIE_API']['URL_CLIENTES'],call='ListarClientes', params={
              "pagina": n+1,
              "registros_por_pagina": 40,
              "apenas_importado_api": "N"
            }).json()
            print(r)
            for i in range(r['registros']):
              dict={}
              cnpj = (r['clientes_cadastro'][i]['cnpj_cpf'])
              codigo_cliente = (r['clientes_cadastro'][i]['codigo_cliente_omie'])
              nome_fantasia = (r['clientes_cadastro'][i]['nome_fantasia'])
              dict.update({
                'cnpj': cnpj,
                'codigo cliente': codigo_cliente,
                'nome fantasia': nome_fantasia
              })
              lista.append(dict)
        return lista
        # pd.DataFrame(lista)
        # df.to_csv('teste_cliente.csv')

    def request_movimentos(api_omie):

        lista = []
        r = api_omie.request(config['OMIE_API']['URL_MOVIMENTO'],call='ListarMovimentos', params={
              "npagina": 1,
              "nRegPorPagina": 100
        }).json()
        print(r['movimentos'])

        for n in range(r['nTotPaginas']):

            r = api_omie.request(config['OMIE_API']['URL_MOVIMENTO'],call='ListarMovimentos', params={
              "npagina": n+1,
              "nRegPorPagina": 100
            }).json()
            print(r)
            for i in range(r['nRegistros']):
              dict={}
              try:
                cnpj = r['movimentos'][i]['detalhes']['cCPFCNPJCliente']
              except:
                  cnpj = ''
              try:
                categoria = r['movimentos'][i]['detalhes']['cCodCateg']
              except:
                  categoria = ''
              try:
                cod_vendedor = r['movimentos'][i]['detalhes']['cCodVendedor']
              except:
                  cod_vendedor = ''
              try:
                grupo = r['movimentos'][i]['detalhes']['cGrupo']
              except:
                  grupo = ''
              try:
                parcela = r['movimentos'][i]['detalhes']['cNumParcela']
              except:
                  parcela = ''
              try:
                status = r['movimentos'][i]['detalhes']['cStatus']
              except:
                  status = ''
              try:
                dt_emissao = r['movimentos'][i]['detalhes']['dDtEmissao']
              except:
                  dt_emissao = '01/01/1000'
              try:
                dt_pagamento = r['movimentos'][i]['detalhes']['dDtPagamento']
              except:
                  dt_pagamento = '01/01/1000'
              try:
                dt_previsao = r['movimentos'][i]['detalhes']['dDtPrevisao']
              except:
                  dt_previsao = '01/01/1000'
              try:
                cod_cliente = r['movimentos'][i]['detalhes']['nCodCliente']
              except:
                  cod_cliente = 0
              try:
                valor = r['movimentos'][i]['detalhes']['nValorTitulo']
              except:
                  valor = ''
              dict.update({
                'cnpj': cnpj,
                'categoria': categoria,
                'codigo vendedor': cod_vendedor,
                'grupo': grupo,
                'parcela': parcela,
                'status': status,
                'data emissao': dt_emissao,
                'data pagamento': dt_pagamento,
                'data previsao': dt_previsao,
                'codigo cliente': cod_cliente,
                'valor': valor
              })
              lista.append(dict)
        return lista
        # df = pd.DataFrame(lista)
        # df.to_csv('teste_movimentos.csv')

    def request_categorias(api_omie):

        lista = []
        r = api_omie.request(config['OMIE_API']['URL_CATEGORIA'],call='ListarCategorias', params={
              "pagina": 1,
              "registros_por_pagina": 100
        }).json()
        for n in range(r['total_de_paginas']):

            r = api_omie.request(config['OMIE_API']['URL_CATEGORIA'],call='ListarCategorias', params={
              "pagina": n+1,
              "registros_por_pagina": 100
            }).json()
            print(r)
            for i in range(r['registros']):
              dict={}
              codigo = r['categoria_cadastro'][i]['codigo']
              categoria = r['categoria_cadastro'][i]['descricao']
              dict.update({
                'codigo': codigo,
                'categoria': categoria
              })
              lista.append(dict)
        return lista
        # df = pd.DataFrame(lista)
        # df.to_csv('teste_categoria.csv')
