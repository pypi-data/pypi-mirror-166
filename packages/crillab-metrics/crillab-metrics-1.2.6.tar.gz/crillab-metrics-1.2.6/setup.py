###############################################################################
#                                                                             #
#  Metrics - rEproducible sofTware peRformance analysIs in perfeCt Simplicity #
#  Copyright (c) 2019-2022 - Univ Artois & CNRS, Exakis Nelite                #
#  -------------------------------------------------------------------------- #
#                                                                             #
#  This program is free software: you can redistribute it and/or modify it    #
#  under the terms of the GNU Lesser General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or (at your #
#  option) any later version.                                                 #
#                                                                             #
#  This program is distributed in the hope that it will be useful, but        #
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY #
#  or FITNESS FOR A PARTICULAR PURPOSE.                                       #
#  See the GNU General Public License for more details.                       #
#                                                                             #
#  You should have received a copy of the GNU Lesser General Public License   #
#  along with this program.                                                   #
#  If not, see <https://www.gnu.org/licenses/>.                               #
#                                                                             #
###############################################################################


"""
Setup script for deploying Metrics on PyPI and allowing to install it using pip.
"""


from setuptools import setup
from typing import List

import metrics


def readme() -> str:
    """
    Reads the README file of the project to use it as long description.

    :return: The long description of Metrics.
    """
    with open('README.md') as file:
        return file.read()


def requirements() -> List[str]:
    """
    Gives the list of the dependencies of the package.

    :return: The dependencies of Metrics.
    """
    return [
        'crillab-autograph',
        'dash-bootstrap-components',
        'deprecated',
        'InquirerPy',
        'jinja2',
        'jsonpickle',
        'loguru',
        'myst-parser',
        'pandas',
        'pyfiglet',
        'pyparsing',
        'pyyaml',
        'tenacity'
    ]


setup(
    name='crillab-metrics',
    version=metrics.__version__,
    packages=[
        'metrics.core',
        'metrics.core.builder',
        'metrics.scalpel',
        'metrics.scalpel.config',
        'metrics.scalpel.parser',
        'metrics.scalpel.utils',
        'metrics.studio',
        'metrics.templates',
        'metrics.wallet',
        'metrics'
    ],

    description=metrics.__summary__,
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords=metrics.__keywords__,

    author=metrics.__author__,
    author_email=metrics.__email__,
    url=metrics.__uri__,

    install_requires=requirements(),

    test_suite='nose.collector',
    tests_require=['nose'],

    scripts=[
        'bin/metrics',
    ],

    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent'
    ],
    license=metrics.__license__,

    package_data={
        'metrics.templates': ['gitignore', '*.ipynb', '*.md', '*.txt', '*.yml']
    },
    include_package_data=True,
    zip_safe=False
)
