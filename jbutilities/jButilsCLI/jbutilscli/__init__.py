#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
client for jbutils

.. currentmodule:: jbutilscli
.. moduleauthor:: Guru Nagarajan <guru@esolve.tech>
"""

from .version import __version__, __release__  # noqa
import os
  
from simple_settings import LazySettings

""" if 'SIMPLE_SETTINGS' in os.environ:
    pass
else:
    os.environ['SIMPLE_SETTINGS']= __file__ + "/settings"
 """
from simple_settings import settings
rpath =  os.path.dirname(__file__)
rpath_parent = os.path.abspath(os.path.join(rpath, os.pardir))

os.environ["PATH"] += os.pathsep + rpath_parent
rfile = "setting"

settings = LazySettings(rfile)


