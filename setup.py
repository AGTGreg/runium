from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="runium",
    version="0.0.1",
    author="Grigoris Chatzinikolaou",
    author_email="greghatzis@gmail.com",
    description="Clean and simple task concurrency",
    long_description="Clean and simple task concurrency, scheduling and repetition for Python",
    url="https://github.com/AGTGreg/runium",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)