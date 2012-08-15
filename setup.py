#!/usr/bin/env python

import commands
from setuptools import setup, find_packages

setup(name="dummyipcp",
      version='0.1',
      description='IPython cluster StarCluster plugin for dummies.',
      author='Dimas Abreu Dutra',
      author_email='dimasadutra@gmail.com',
      url='http://github.com/dimasad/dummyipcp',
      test_suite='nose.collector',
      tests_require=['nose>=1.0'],
      install_requires='distribute',
      packages=find_packages())
