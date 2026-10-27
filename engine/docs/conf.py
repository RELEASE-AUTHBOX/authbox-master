_A='sphinx_rtd_theme'
import os,sys
sys.path.insert(0,os.path.abspath('..'))
project='AUTHBOX'
copyright='2024, Iwan Setiawan'
author='Iwan Setiawan'
release='1.0'
extensions=['sphinx.ext.autodoc',_A]
templates_path=['_templates']
exclude_patterns=['_build','Thumbs.db','.DS_Store','__pycache__','**/*.migrations.rst','__init.py__','migrations*']
html_theme=_A
html_static_path=['_static']