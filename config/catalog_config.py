import configparser

from config.env_interpolation import EnvInterpolation


class CatalogConfig(configparser.ConfigParser):
    def __init__(self):
        super().__init__(interpolation=EnvInterpolation())

    def read(self, filenames='config.ini', *args, **kwargs):
        super().read(filenames, *args, **kwargs)
