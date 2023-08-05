"""Simplified units."""

import pkg_resources as pkg  # part of setuptools

package = "numcertainties"

try:
    version = pkg.require(package)[0].version
except pkg.DistributionNotFound:
    version = "dirty"

__version__ = version

from .core import *
from .num_units import *
