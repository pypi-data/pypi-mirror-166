from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION="JUST A SAMPLE HELLO PACKAGE"

setup(
    name="hello-dummy",
    version=VERSION,
    author="Lokji",
    author_email="<temp@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(), 
    install_requires=['numpy'],
    keywords=['python','numpy'],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]
)
