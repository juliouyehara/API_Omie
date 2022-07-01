from config.catalog_config import CatalogConfig
import requests as re

config = CatalogConfig()
config.read()
print(config['OMIE_API']['URL'])
