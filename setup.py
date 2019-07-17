import os
import codecs
from setuptools import setup, find_packages


CURRENT_VERSION = "0.1.6"


def read_file(filename):
    """
    Read a utf8 encoded text file and return its contents.
    """
    with codecs.open(filename, 'r', 'utf8') as f:
        return f.read()


setup(
    name="runium",
    version=CURRENT_VERSION,
    author="Grigoris Chatzinikolaou",
    author_email="greghatzis@gmail.com",
    description="Clean and simple task concurrency for Python.",
    long_description=read_file('README.md'),
    keywords=[
        'concurrecy', 'asynchonous', 'tasks', 'scheduling', 'scheduler',
        'cron', 'multiprocessing', 'multithreading', 'callbacks',
        'non-blocking'
    ],
    url="https://github.com/AGTGreg/runium",
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
