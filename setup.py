#!/usr/bin/env python3
from setuptools import setup

setup(
    name="RSI.py",
    version="1.2.0",
    description="A library for manipulation of the RSI format used in Space Station 14.",
    url="https://github.com/space-wizards/RSI.py",
    author="Pieter-Jan Briers",
    author_email="pieterjan.briers@gmail.com",
    license="MIT",
    packages=["rsi"],
    python_requires=">=3.5",
    install_requires=[
        "Pillow"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    project_urls={
        "Source": "https://github.com/space-wizards/RSI.py"
    },
    entry_points={'console_scripts': ['rsi=rsi.__main__:main']},
)
