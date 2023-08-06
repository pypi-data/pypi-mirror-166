#!/usr/bin/env python

from setuptools import setup

setup(name='voice_python',
      version='0.1',
      description='Python implementation of the vOICe (seeingwithsound) in Python',
      url='http://github.com/ruizserra/vOICe-python',
      author='Jaime Ruiz Serra',
      author_email='',
      license='MIT',
      install_requires=[
          'numpy',
          'opencv-python'
      ],
      zip_safe=False)
