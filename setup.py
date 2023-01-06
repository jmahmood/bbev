__author__ = 'jawaad'

from distutils.core import setup

setup(name='bbev',
      version='0.0.2',
      description='Using the Wii Balance Board with Linux\'s EVDev interface.',
      author='Jawaad Mahmood',
      author_email='ideas@jawaadmahmood.com',
      url='https://github.com/jmahmood/bbev/',
      packages=['bbev'], requires=['evdev'])