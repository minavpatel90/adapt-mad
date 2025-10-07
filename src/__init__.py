"""
ADAPT-MAD: Adaptive Multi-Agent Detection Framework
"""

__version__ = "1.0.0"
__author__ = "Minav Suresh Patel, Rohit Dhawan, Ankush Dhar"

from . import agents
from . import coordination
from . import models
from . import utils

__all__ = ['agents', 'coordination', 'models', 'utils']
