from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.2'
DESCRIPTION = 'Hello from NED'
LONG_DESCRIPTION = 'A package that says hello from NED.'

# Setting up
setup(
    name="hello_from_ned",
    version=VERSION,
    author="Adnan Khan",
    author_email="<mail@abc.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'hello','ned'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)