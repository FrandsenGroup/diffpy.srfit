#!/usr/bin/env python
##############################################################################
#
# diffpy.srfit      by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2008 The Trustees of Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE_DANSE.txt for license information.
#
##############################################################################

"""
Definition of __version__, __date__, __timestamp__, __git_commit__.

Notes
-----
Variable `__gitsha__` is deprecated as of version 3.0.
Use `__git_commit__` instead.
"""

__all__ = ['__date__', '__git_commit__', '__timestamp__', '__version__']

from pkg_resources import resource_filename
from configparser import RawConfigParser


# obtain version information from the version.cfg file
cp = RawConfigParser(dict(version='', date='', commit='', timestamp=0))
if not cp.read(resource_filename(__name__, 'version.cfg')):
    from warnings import warn
    warn('Package metadata not found, execute "./setup.py egg_info".')

__version__ = cp.get('DEFAULT', 'version')
__date__ = cp.get('DEFAULT', 'date')
__git_commit__ = cp.get('DEFAULT', 'commit')
__timestamp__ = cp.getint('DEFAULT', 'timestamp')

# TODO remove in version 3.1.
__gitsha__ = __git_commit__

del cp

# End of file
