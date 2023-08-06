from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'wrapper for pyreadstat'
LONG_DESCRIPTION = 'wrapper for pyreadstat to easily read, create, and adjust .sav files'

# Setting up
setup(
    name="prs-meta",
    version=VERSION,
    author="DvGils",
    author_email="<demian_vg@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyreadstat', 'pandas'],
    keywords=['python', 'pyreadstat', 'SPSS', 'sav', 'meta', 'meta data'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

