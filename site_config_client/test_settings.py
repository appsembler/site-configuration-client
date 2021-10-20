"""
Pytest settings to use mock dir for modules in edx-platform
"""
import sys
from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


sys.path.append(root('mocks'))
