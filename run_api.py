from omie import *
from config.catalog_config import CatalogConfig

config = CatalogConfig()
config.read()

print(config['OMIE_API']['URL'])

api_omie = ApiOmie(config['OMIE_KEY']['URL'], config['OMIE_SECRETS']['URL'])
# for i in range(20):
#     r = api_omie.request(config['OMIE_API']['URL'],call='ListarContasReceber', params={
#       "pagina": i+1,
#       "registros_por_pagina": 500,
#       "apenas_importado_api": "N"
#     }).json()
#
#     print(r)

r = api_omie.request(config['OMIE_API']['URL_VENDEDORES'],call='ListarVendedores', params={
  "pagina": 1,
  "registros_por_pagina": 40,
  "apenas_importado_api": "N"
}).json()



