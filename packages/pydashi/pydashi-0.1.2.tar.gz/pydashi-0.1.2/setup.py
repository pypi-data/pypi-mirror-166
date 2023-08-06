import os
import re

from setuptools import setup

def get_version(package):
    """ 
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, '__init__.py'), 'rb') as init_py:
        src = init_py.read().decode('utf-8')
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", src).group(1)

version = get_version('dashi')

setup(
    name = "pydashi",
    version = version,
    author = "The dashi developers",
    author_email = "eike@middell.net",
    description = ("TODO"),
    license = "LGPL",
    #keywords = "histograms fitting ",
    url = "https://github.com/emiddell/dashi",
    packages=['dashi', 'dashi.tests', 'dashi.datasets'],
    long_description='TODO',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 2.7"
    ],
)
