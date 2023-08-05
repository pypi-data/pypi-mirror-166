from setuptools import setup

long_description = """mapascii
========

A simple array-based class used for maps

Installation
------------

.. line-block::

  pip install mapascii

Usage Example
-------------

.. code:: python

  from mapascii import Map
  
  #create and display map
  #Map(/, columns: int, rows: int, *, empty=' ', clear_screen=False, pixel_size=1)
  map = Map(10, 10, empty='#', clear_screen=True)
  map[5,5] = '$'
  print(map)
  
  Output:
  
  ##########
  ##########
  ##########
  ##########
  ##########
  #####$####
  ##########
  ##########
  ##########
  ##########
  
  Output was squashed because characters are half as wide as they are long."""

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Multimedia :: Graphics',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3'
]

setup(name='mapascii',
      version='1.0.2',
      description='A small array-based class for maps',
      long_description=long_description,
      author='meiscool466',
      author_email='meiscool466@gmail.com',
      classifiers=CLASSIFIERS,
      keywords='array class maps ascii'
)
