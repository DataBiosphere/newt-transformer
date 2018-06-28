import os

from setuptools import setup, find_packages
from release import read_version


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="newt-transformer",
    description="Amphibious new data transformer to prepare various sources for CGP DSS Data Loader",
    packages=find_packages(),  # include all packages under newt
    url="https://github.com/DataBiosphere/newt-transformer",
    entry_points={
        'console_scripts': [
            'newt=newt.main:main'
        ]
    },
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=[
        'jsonschema >=2.6, <3'
    ],
    license='Apache License 2.0',
    include_package_data=True,
    zip_safe=True,
    author="Jesse Brennan",
    author_email="brennan@ucsc.edu",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    version='{}.{}.{}'.format(*read_version()),
    keywords=['genomics', 'metadata', 'NIHDataCommons'],
    # Use setuptools_scm to set the version number automatically from Git
)
