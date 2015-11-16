#!/usr/bin/env python

from distutils.core import setup

with open('README.md', 'r') as f:
    desc = f.read()

setup(name='name2time',
      version='0.2',
      description=desc,
      author='Aleksandar Ristic',
      author_email='aleksandar.ristic1983@gmail.com',
      url='https://github.com/aleksandarristic/name2time/',
      packages=['name2time'],
      scripts=['scripts/name2timestamp']
      )
