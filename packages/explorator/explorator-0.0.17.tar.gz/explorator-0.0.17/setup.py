import sys
import os
from setuptools import setup

from explorator.general_info import _version

setup(
    name='explorator',
    version=_version,
    description='Package to quickly explore data in pandas dataframe',
    license='',
    packages=['explorator'],
    author='Boris Protoss',
    author_email='bz@cro.team',
    keywords=['pandas','exploratory'],
    url=''
)
