"""
setup script for ezsaver package

https://github.com/EricThomson/ezsaver
"""

from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

setup(
    name='ezsaver',
    version='0.1.0',
    description="Save stuff quick and easy in Python",
    author="Eric Thomson",
    author_email="thomson.eric@gmail.com",
    licence="MIT",
    url="https://github.com/EricThomson/ezsaver",
    packages=find_packages(include=['ezsaver', 'ezsaver.*']),
    install_requires=[
        'joblib',
        'varname'],
    long_description=long_description,
    long_description_content_type="text/markdown"
)
