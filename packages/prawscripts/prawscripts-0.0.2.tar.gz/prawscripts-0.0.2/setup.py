from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Compilation of PRAW scripts built over the years by the community'

# Setting up
setup(
    name="prawscripts",
    version=VERSION,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['praw'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)
