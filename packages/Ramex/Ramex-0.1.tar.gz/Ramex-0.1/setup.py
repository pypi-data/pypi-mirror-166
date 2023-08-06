#!/usr/bin/env python

from setuptools import setup

setup(
    name='Ramex',
    version='0.1',
    description='Ultimate Member Adding Tool for Telegram',
    author='@Annex_xD',
    license="GPLv3",
    scripts=['ramex'],
    install_requires=["requests", "lolpython", "colorama", "telethon", "pyfiglet"]
)
