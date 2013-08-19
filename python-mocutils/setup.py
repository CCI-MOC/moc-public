from distutils.core import setup

setup(name='mocutils',
      version='0.1',
      scripts=[
        'scripts/power_cycle.py',
        'scripts/move_headnode.py',
        'scripts/vm-vlan',
	'scripts/boot-default.py'
        ]
      )
