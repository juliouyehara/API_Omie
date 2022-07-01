import os
import configparser


class EnvInterpolation(configparser.BasicInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        return os.path.expandvars(value)
