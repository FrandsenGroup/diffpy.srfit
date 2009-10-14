########################################################################
#
# diffpy.srfit      by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2008 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
########################################################################

"""The core equation evaluator for diffpy.srfit.

This package contains modules and subpackages that are used to create Equation
objects. An Equation is a functor that remembers its state, and that can
quickly re-evaluate its value based on changes in its variables. Equations can
be used to encapsulate simple expressions or complex signal generators,
provided one gets to know how to create and use Literal classes (from the
literals subpackage), that are the basic building blocks of an Equation.

Packages:
literals    --  The literals subpackage contains various Literal classes.
                Literals are composed to create a Literal tree, which is the
                decomposition of an equation into Operators, Arguments, and
                more exotic building blocks.  See the package documentation for
                more details.
visitors    --  The visitors subpackage contains Visitor classes that can
                extract various properties from a Literal tree. The most
                important Visitor is the Evaluator, which evaluates the Literal
                tree.  See the package documentation for more details.

Modules:
builder     --  The builder module contains classes and methods that aid in the
                construction of Equations. There are options for creating an
                Equation from a string, or from EquationBuilder objects.  See
                the module documentation for a discription of these tools.
equationmod --  The equationmod module contains the Equation class (see below).

Classes:
Equation    --  Equations encapsulate a Literal tree and an Evaluator that can
                walk the tree and evaluate its value.  Equations check the
                validity of a Literal and give attribute-like access to the
                Arguments of the literal tree. Examples of Equation use can be
                found in the Equation module documentation.

"""

from builder import EquationFactory

# package version
from diffpy.srfit.version import __version__

# End of file
