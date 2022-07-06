from omie import *
from config.catalog_config import CatalogConfig
from pprint import pprint
import pandas as pd


config = CatalogConfig()
config.read()

print(config['OMIE_API']['URL'])

api_omie = ApiOmie(config['OMIE_KEY']['URL'], config['OMIE_SECRETS']['URL'])


lista = []
for n in range(251):
    r = api_omie.request(config['OMIE_API']['URL'],call='ListarContasReceber', params={
          "pagina": n+1,
          "registros_por_pagina": 40,
          "apenas_importado_api": "N"
        }).json()
    print(r)
    for i in range(40):
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

r = api_omie.request(config['OMIE_API']['URL_VENDEDORES'],call='ListarVendedores', params={
  "pagina": 1,
  "registros_por_pagina": 40,
  "apenas_importado_api": "N"
}).json()

for i in range(29):
  dict = {}
  print(r['cadastro'][i])
  codigo_vendedor = (r['cadastro'][i]['codigo'])
  nome_vendedor = (r['cadastro'][i]['nome'])
  dict.update({'codigo vendedor': codigo_vendedor,
               'nome vendedor': nome_vendedor
               })
  lista.append(dict)
df = pd.DataFrame(lista)
df.to_csv('teste_vendedores.csv')

r = api_omie.request(config['OMIE_API']['URL_CLIENTES'],call='ListarClientes', params={
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
df = pd.DataFrame(lista)
df.to_csv('teste_cliente.csv')

r = api_omie.request(config['OMIE_API']['URL_MOVIMENTO'],call='ListarMovimentos', params={
      "npagina": 1,
      "nRegPorPagina": 100
}).json()

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
          dt_emissao = ''
      try:
        dt_pagamento = r['movimentos'][i]['detalhes']['dDtPagamento']
      except:
          dt_pagamento = ''
      try:
        dt_previsao = r['movimentos'][i]['detalhes']['dDtPrevisao']
      except:
          dt_previsao = ''
      try:
        cod_cliente = r['movimentos'][i]['detalhes']['nCodCliente']
      except:
          dt_previsao = ''
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
df = pd.DataFrame(lista)
df.to_csv('teste_movimentos.csv')
