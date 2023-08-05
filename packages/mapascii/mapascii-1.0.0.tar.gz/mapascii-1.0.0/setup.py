from setuptools import setup

with open('DESCRIPTION.txt') as f:
    long_description = f.read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Multimedia :: Graphics',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3'
]

setup(name='mapascii',
      version='1.0.0',
      description='A small array-based class for maps',
      long_description=long_description,
      author='meiscool466',
      author_email='meiscool466@gmail.com',
      classifiers=CLASSIFIERS,
      keywords='array class maps ascii'
)
