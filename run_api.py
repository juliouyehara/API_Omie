from enpoints import *
from config.catalog_config import CatalogConfig
from postgres import *
import pandas as pd
import sched

scheduler = sched.scheduler()

config = CatalogConfig()
config.read()

api_omie = ApiOmie(config['OMIE_KEY']['URL'], config['OMIE_SECRETS']['URL'])

lista_categorias = Endpoint.request_categorias(api_omie)

lista_movimentos = Endpoint.request_movimentos((api_omie))

lista_clientes = Endpoint.request_clientes(api_omie)

lista_vendedores = Endpoint.request_vendedores(api_omie)

df_vendedores = pd.DataFrame(lista_vendedores)
df_categorias = pd.DataFrame(lista_categorias)
df_clientes = pd.DataFrame(lista_clientes)
df_movimentos = pd.DataFrame(lista_movimentos)
# print(lista_categorias)
# print(df_categorias)

# print(lista_movimentos)
# print(df_movimentos)
# insert_postgre_elastic('postgres://postgres:master01@localhost:5432/postgres', r)
lista_cnpj = []
lista_nome = []
# def modelagem(df_movimentos, df_categorias, df_clientes, df_vendedores):
def modelagem(df_movimentos, df_clientes, df_categorias, df_vendedores):
    for i in df_movimentos['codigo cliente']:
        cnpj = df_clientes['cnpj'][df_clientes['codigo cliente'] == i]
        nome = df_clientes['nome fantasia'][df_clientes['codigo cliente'] == i]
        nome = str(nome)
        nome = nome.split()[1:]
        nome = nome[:-5]
        nome = ','.join(nome)
        nome = nome.replace(',', ' ')
        lista_cnpj.append(cnpj)
        lista_nome.append(nome)
    df_movimentos['nome fantasia']  = lista_nome

    lista_categoria = []
    for i in df_movimentos['categoria']:
        categoria = df_categorias['categoria'][df_categorias['codigo'] == i]
        categoria = str(categoria)
        categoria = categoria.split()[1:]
        categoria = categoria[:-4]
        categoria = ','.join(categoria)
        categoria = categoria.replace(',', ' ')
        lista_categoria.append(categoria)
    df_movimentos['nome categoria'] = lista_categoria
    lista_vendedor = []
    for i in df_movimentos['codigo vendedor']:
        if i == 0:
            vendedor = '0'
        else:
            vendedor = df_vendedores['nome vendedor'][df_vendedores['codigo vendedor'] == i]
        vendedor = str(vendedor)
        vendedor = vendedor.split()[1:]
        vendedor = vendedor[:-5]
        vendedor = ','.join(vendedor)
        vendedor = vendedor.replace(',', ' ')
        lista_vendedor.append(vendedor)
    df_movimentos['vendedores'] = lista_vendedor
    df_movimentos = df_movimentos.fillna(0)
    df_dict = df_movimentos.to_dict('records')

    insert_postgre_elastic('postgres://Julio:Metaverso1@35.199.78.144:5432/AccountfyTeste', df_dict)
    scheduler.enter(delay=1000, priority=0, action=modelagem())

modelagem()
scheduler.run(blocking=True)


# schedule.every().day.at("10:30").do(modelagem)
