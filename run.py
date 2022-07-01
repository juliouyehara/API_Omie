from config.catalog_config import CatalogConfig

config = CatalogConfig()
config.read()
print(config['OMIE_API']['URL'])
