try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
	
config = {
	'description': 'Wrapper classes for PsychoPy stimuli',
	'author': 'Steve Loria',
	'url': 'https://github.com/sloria/stimulus.py',
	'author_email': 'sloria1@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['psychopy'],
	'py_modules': ['stimulus'],
	'name': 'stimulus.py',
}

setup(**config)