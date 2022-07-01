from config.catalog_config import CatalogConfig

config = CatalogConfig()
config.read()

print(config['EMAIL']['URI'])