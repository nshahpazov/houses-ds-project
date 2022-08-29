"""The API Module"""
import pathlib

from . import api

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
VERSION_PATH = PACKAGE_ROOT / 'VERSION'


with open(VERSION_PATH, 'r', encoding='utf-8') as version_file:
    __version__ = version_file.read().strip()
