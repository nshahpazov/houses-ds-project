"""setup our houses_pipeline package"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
from pathlib import Path
from setuptools import find_packages, setup

# Package meta-data.
NAME = 'houses_pipeline'
DESCRIPTION = "Houses pipeline for preprocessing and training a model"
URL = 'https://github.com/nshahpazov/houses-ds-project'
EMAIL = 'nshahpazov@gmail.com'
AUTHOR = 'Nikola Shahpazov'
REQUIRES_PYTHON = '>=3.9.2'


# def list_reqs(fname='requirements.txt'):
#     """Packages that are required for this module to be executed"""
#     with open(fname, encoding="utf-8") as descriptor:
#         return descriptor.read().splitlines()


here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as file:
        LONG_DESCRIPTION = '\n' + file.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION


# Load the package's __version__.py module as a dictionary.
ROOT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = ROOT_DIR / 'houses_pipeline'
about = {}

with open(PACKAGE_DIR / 'VERSION', encoding='utf-8') as file:
    _version = file.read().strip()
    about['__version__'] = _version


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    # package_dir={'': PACKAGE_DIR},
    package_data={'houses_pipeline': ['VERSION']},
    # install_requires=list_reqs(),
    extras_require={
        "dev": ["pytest>=7.1.2"]
    },
    include_package_data=True,
    license='BSD 3',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
