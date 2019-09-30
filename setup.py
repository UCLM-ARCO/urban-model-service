#!/usr/bin/python3
# -*- mode: python; coding: utf-8 -*-

from distutils.core import setup

__version__ = '0.1'
exec(open('version.py').read())

setup(
    name          = 'urban-model-service',
    version       =  __version__,
    description   = "Services that allow queries about a model based on the IndoorGML standard",
    author        = "Arco Group",
    author_email  = "arco.group@gmail.com",
    url           = "https://bitbucket.org/arco_group/urban-model-service",
    # packages      = ['lib'],
    scripts       = ['src/urban-model-server'],
    package_dir   = {'': 'src'},
    py_modules    = ["openlocationcode", "IndoorGMLreader"],
    data_files    = [
        ("share/slice/urban-model/", ["slice/UrbanService.ice"])
    ],
)
