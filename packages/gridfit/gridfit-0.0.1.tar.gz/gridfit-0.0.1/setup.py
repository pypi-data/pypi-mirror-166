#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    "numpy",
    "scipy",
    "tqdm"
]

test_requirements = ['pytest>=3', ]

setup(
    author="Tingkai Liu",
    author_email='tingkai.liu@columbia.edu',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    description="A Python port of the gridfit function in MATLAB exchange.",
    install_requires=requirements,
    license="BSD license",
    include_package_data=True,
    keywords='gridfit',
    name='gridfit',
    packages=find_packages(include=['gridfit', 'gridfit.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/TK-21st/PyGridFit',
    version='0.0.1',
    zip_safe=False,
)
