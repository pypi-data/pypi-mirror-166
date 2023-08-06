__version__ = '0.1.0'

from .plugins import register as plugin_register

def register():
    plugin_register()

register()