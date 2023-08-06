from setuptools import setup, find_packages
from pathlib import Path

NAME = 'oxbuster'
DESCRIPTION = 'A Handy Script for Finding Website Directories using Wordlists'
TAG = ['dir', 'buster', 'wordlist']
REQUIREMENT = ['oxansi', 'oxflags']

VERSION = '0.0.3'
LONG_DESCRIPTION = (Path(__file__).parent / "README.md").read_text()

setup(
    name=NAME,
    version=VERSION,
    author="0x68616469",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
		long_description=LONG_DESCRIPTION,    
		packages=find_packages(),
    install_requires=REQUIREMENT,
    keywords=TAG,
    entry_points = {'console_scripts': ['oxbuster = oxbuster:main']},
    classifiers=[
		"Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)