#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'cal_star'
DESCRIPTION = 'This project is used for standard star filed calibration.'
URL = 'https://github.com/git-yuliang/standard_star.git'
#URL = 'https://pypi.org/project/cal-star/'
EMAIL = "liangyuak@163.com",#"yuliang@shao.ac.cn",
AUTHOR = "Yu Liang",
REQUIRES_PYTHON = '>=3.7.0'
VERSION = '0.1.2'

# What packages are required for this module to be executed?
REQUIRED = [
    'pandas>=1.3.3',
    'numpy>=1.21.6',
    'matplotlib>=3.2.2',
    'astropy>=4.3.1',
    'scipy>=1.5.0',
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email="yuliang@shao.ac.cn",
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(where="src"),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    #include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={'upload': UploadCommand,
    },      
    package = {'cal_star'},
    package_dir={'cal_star': 'src/cal_star'},
    package_data={'cal_star': [ 
                        './refdata/1d_sp/Hamuy1992/*.dat',
                        './refdata/1d_sp/oke1990/*.dat',
                        './refdata/1d_sp/Massey1998/*.dat',
                        './refdata/1d_sp/ctiocal/*.dat',
                        './refdata/1d_sp/gemini/*.dat',
                        './refdata/starlists/Hamuy1992/*.xlsx',
                        './refdata/starlists/oke1990/*.xlsx',
                        './refdata/starlists/Massey1998/*.xlsx',
                        './refdata/starlists/ctiocal/*.xlsx',
                        './refdata/starlists/gemini/*.xlsx',
                        './refdata/Photometric/Landolt1992/*.xlsx',
                        './refdata/clusters/NGC6397/*.tif',
                        './refdata/clusters/NGC6397/*.fits',
                        './refdata/clusters/NGC6397/*.xlsx',
                        './refdata/clusters/NGC6540/*.tif',
                        './refdata/clusters/NGC6540/*.jpg',
                        './refdata/clusters/NGC6540/*.xlsx',
                        './refdata/clusters/47Tuc_NGC104/*.tif',
                        './refdata/clusters/47Tuc_NGC104/*.jpg',
                        './refdata/clusters/47Tuc_NGC104/*.xlsx', 
                        './refdata/clusters/NGC6752/*.tif',
                        './refdata/clusters/NGC6752/*.jpg',
                        './refdata/clusters/NGC6752/*.xlsx',   
                        './refdata/clusters/NGC6121/*.tif',
                        './refdata/clusters/NGC6121/*.jpg',
                        './refdata/clusters/NGC6121/*.xlsx',                          
                        './demo/*.ipynb',
                        './demo/*.py',
     ]},  
)