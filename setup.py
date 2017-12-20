import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


install_requires = [
    line
    for line in open(
        os.path.join(here, "requirements.txt"),
        "r"
    )
]
author = 'ryankung'
email = 'ryankung@ieee.org'


setup(
    name='celebi',
    description='celebi is a Actor Based TS data anaylize engine',  # noqa
    version='0.0.1',
    packages=find_packages(here, exclude=['tests']),
    license='GPL',
    author=author,
    author_email=email,
    install_requires=install_requires,
)
