import os

import setuptools
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setuptools.setup(
    name= "aditya_string_uppercase",
    version= "0.0.1",
    author= "Aditya Gupta",
    author_email="adityagupta9293@gmail.com",
    description="make strings uppercase and concatenate them",
    python_requires='>=3.6',
    packages=["aditya_custom_package"]
)