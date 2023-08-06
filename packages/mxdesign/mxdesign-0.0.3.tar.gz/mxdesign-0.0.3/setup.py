#!/usr/bin/env python

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read().strip()

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().strip().split('\n')

setuptools.setup(
    name='mxdesign',
    version='0.0.3',
    author='Yasas Senarath',
    author_email='wayasas@gmail.com',
    description='A framework for eXperiment design specification',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ysenarath/mxdesign',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    include_package_data=True,
)
