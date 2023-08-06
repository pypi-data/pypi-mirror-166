#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "base58",
    "py-multibase",
    "py-multicodec",
    "morphys",
    "planetmint-multiformat-multihash",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest",
    "pytest-cov",
    "hypothesis",
]

setup(
    name="planetmint-py-cid",
    version="0.4.2",
    description="Self-describing content-addressed identifiers for distributed systems",
    long_description=readme + "\n\n" + history,
    author="Dhruv Baldawa",
    author_email="mail@planetmint.io",
    url="https://github.com/planetmint/py-cid",
    packages=find_packages(include=["cid"]),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords="cid",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    test_suite="tests",
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
