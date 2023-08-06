"""Simplified uncertainties."""

import pkg_resources as pkg  # part of setuptools

package = "numcertainties"

try:
    version = pkg.require(package)[0].version
except pkg.DistributionNotFound:
    version = "dirty"

__version__ = version

from .base import *
from .jacobian import *
from .semi_analytic import *
from .monte_carlo import *