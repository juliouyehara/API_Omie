from enpoints import *
from config.catalog_config import CatalogConfig

config = CatalogConfig()
config.read()

api_omie = ApiOmie(config['OMIE_KEY']['URL'], config['OMIE_SECRETS']['URL'])

Endpoint.request_categorias(api_omie)

Endpoint.request_movimentos((api_omie))

Endpoint.request_clientes(api_omie)

Endpoint.request_vendedores(api_omie)