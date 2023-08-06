#!/usr/bin/env python
from setuptools import setup

setup(name='pyscrabbler',
      version='1.1.1',
      description='Provide a set of letters and retrieve a list of potential words and point values for Scrabble.',
      author='Michael Warmbier',
      author_email='business@michaelwarmbier.com',
      url='http://michaelwarmbier.com',
      data_files=[('', ['Dictionary.txt'])],
      package_data={'': ['Dictionary.txt']},
      include_package_data=True,
     )