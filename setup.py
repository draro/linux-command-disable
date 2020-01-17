# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='disable_commands',
      version='0.1',
      description='Disable Linux commands',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='#',
      author='Davide Raro',
      author_email='davide.raro@me.com',
      license='MIT',
      packages=['disable_commands'],
      zip_safe=False)
