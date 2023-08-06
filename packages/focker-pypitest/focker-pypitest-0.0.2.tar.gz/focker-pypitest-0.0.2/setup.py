#!/usr/bin/env python3
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="focker-pypitest",
    version="0.0.2",
    author="Felix Ocker",
    author_email="felix.ocker@googlemail.com",
    description="intended for testing release automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felixocker/focker-pypitest",
    project_urls={
        "Bug Tracker": "https://github.com/felixocker/focker-pypitest/issues",
    },
    download_url="https://github.com/felixocker/focker-pypitest/archive/refs/tags/v0.0.2.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    keywords=["release", "pypi", "test"],

    include_package_data=True,  # include non-code files during installation
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
    ],
)

