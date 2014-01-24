
from setuptools import setup
setup(name='spl',
      version='1.0',
      url='https://github.com/CCI-MOC/moc-public',
      packages=['spl'],
      scripts=['spl_init.py', 'spl_restful.py', 'spl_shell.py'],
      install_requires=[
          'flask',
          'libvirt-python',
          'sqlalchemy',
          'Flask-HTTPAuth',
      ],
      )
