from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.7'
DESCRIPTION = 'Python Package Used By KEA - Copenhagen School of Design and Technology'
LONG_DESCRIPTION = 'Different python packages to used by students of KEA - Copenhagen School of Design and Technology'

# Setting up
setup(
    name="pykea",
    version=VERSION,
    license='MIT',
    author="Sofian Hanash",
    author_email="soha@kea.dk",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python', 'beackhoff', 'ads'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)