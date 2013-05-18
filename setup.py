try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
	
config = {
	'description': 'Wrapper classes for PsychoPy stimuli',
	'author': 'Steve Loria',
	# 'url': 'URL to get it at',
	'author_email': 'sloria1@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['psychopy'],
	'name': 'stimulus.py'
}

setup(**config)