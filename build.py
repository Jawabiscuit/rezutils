"""Utilities that can be used at build-time by a package.py"""
import re
from rez.exceptions import InvalidPackageError


def validate(this, **data):
    """Ensure packages meet certain requirements
    
    Args:
        data (dict): Key / values of package string and function attributes
        this (DeveloperPackage): Rez package object 
    """
    regex = re.compile("[a-zA-Z_]+$")
    if not regex.match(this.name):
        raise InvalidPackageError("Invalid package name.")
