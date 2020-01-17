from setuptools import setup, find_packages
from os import path
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
