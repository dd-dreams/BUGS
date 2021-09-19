from setuptools import setup, find_packages
from scripts.constants.messages import LONG_DESCRIPTION, DESCRIPTION


setup(
    name='BUGS',
    version='0.0.0',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/dd-dreams/BUGS',
    author='dd-dreams',
    license='MIT',
    packages=find_packages()
)

