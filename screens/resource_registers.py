'''Resource register for a screens module.'''
# forked from https://github.com/rafalo1333/KivyLazyloadingExample

import os.path
from kivy.resources import resource_add_path

_base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
'''Path of the application's root.'''

_data_paths = (
    'data/images',
    'data/fonts',
    'data/audio'
)
'''Paths of the data dirs.'''

_kv_paths = ('kv', )
'''Paths of the kv dirs.'''

_registered = False
'''Indicates if the resources has been registered.'''

def register_kv_and_data():
    '''Registers the data and kv paths in Kivy resources system.'''
    global _registered
    if _registered:
        return
    for path in _data_paths + _kv_paths:
        p = os.path.join(_base_path, path)
        resource_add_path(p)
    _registered = True
