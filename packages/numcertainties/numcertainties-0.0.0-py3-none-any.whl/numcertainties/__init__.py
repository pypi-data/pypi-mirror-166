"""Simplified uncertainties."""

import pkg_resources as pkg  # part of setuptools

package = "numcertainties"

try:
    version = pkg.require(package)[0].version
except pkg.DistributionNotFound:
    version = "dirty"

__version__ = version

from .unc import *
from .nunc import *
from .uunc import *
from .munc import *