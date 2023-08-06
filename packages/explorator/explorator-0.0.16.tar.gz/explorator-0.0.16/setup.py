import sys
import os
from setuptools import setup

sys.path.append(os.path.abspath(f"{os.environ['ONEDRIVE']}\\Documents\\Python_Scripts\\workfolder\\lanit_omni\\explorator\\datae\\explorator_library\\explorator"))

from general_info import _version

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
