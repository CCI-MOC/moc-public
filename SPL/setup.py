
from setuptools import setup, find_packages
setup(name='spl',
      version='1.0',
      py_modules=['spl_control','spl_er','spl_command_pattern','spl_config'],
      install_requires=['flask','sqlalchemy','Flask-HTTPAuth'],
      )
