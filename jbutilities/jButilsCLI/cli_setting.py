

""" if 'SIMPLE_SETTINGS' in os.environ:
    pass
else:
    os.environ['SIMPLE_SETTINGS']= __file__ + "/settings"
 """
 
import os
from simple_settings import settings
from simple_settings import LazySettings

class cli_Settings:
    def __init__(self):
      
        rpath =  os.path.dirname(__file__)
        rpath_parent = os.path.abspath(os.path.join(rpath, os.pardir))
        os.environ["PATH"] += os.pathsep + rpath
        os.environ["PATH"] += os.pathsep + rpath_parent
        os.environ["PATH"] += os.pathsep + rpath + '\\utils24'
        
        rfile = "setting"

        clisettings = LazySettings(rfile)
        self.clisettings=clisettings

    def get_settings(self):

        return self.clisettings
