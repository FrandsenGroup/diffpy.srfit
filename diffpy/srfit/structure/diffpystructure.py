#!/usr/bin/env python
########################################################################
#
# diffpy.srfit      by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2009 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
########################################################################
"""Wrappers for interfacing a diffpy.Structure.Structure with SrFit.

A diffpy.Structure.Structure object is meant to be passed to a StrucureParSet
object from this module, which can then be used as a ParameterSet. Any change
to the lattice or existing atoms will be registered with the Structure. Changes
in the number of atoms will not be recognized. Thus, the
diffpy.Structure.Structure object should be fully configured before passing it
to Structure.

StructureParSet --  Adapter for diffpy.Structure.Structure
LatticeParSet   --  Adapter for diffpy.Structure.Lattice
AtomParSet      --  Adapter for diffpy.Structure.Atom

"""
__id__ = "$Id$"

from diffpy.srfit.fitbase.parameter import Parameter, ParameterProxy
from diffpy.srfit.fitbase.parameter import ParameterWrapper
from diffpy.srfit.fitbase.parameterset import ParameterSet
from diffpy.srfit.structure.basestructure import BaseStructure

# Accessor for xyz of atoms
def _xyzgetter(i):

    def f(atom):
        return atom.xyz[i]

    return f

def _xyzsetter(i):

    def f(atom, value):
        atom.xyz[i] = value
        return

    return f


class AtomParSet(ParameterSet):
    """A wrapper for diffpy.Structure.Atom.

    This class derives from diffpy.srfit.fitbase.parameterset.ParameterSet. See
    this class for base attributes.

    Attributes:
    atom        --  The diffpy.Structure.Atom this is adapting
    element     --  The element name (property).

    Managed Parameters:
    x (y, z)    --  Atom position in crystal coordinates (ParameterWrapper)
    occupancy   --  Occupancy of the atom on its crystal location
                    (ParameterWrapper)
    occ         --  Proxy for occupancy (ParameterProxy).
    U11, U22, U33, U12, U21, U23, U32, U13, U31
                --  Anisotropic displacement factor for atom (ParameterWrapper
                    or ParameterProxy). Note that the Uij and Uji parameters
                    are the same.
    Uiso        --  Isotropic ADP (ParameterWrapper).
    B11, B22, B33, B12, B21, B23, B32, B13, B31
                --  Anisotropic displacement factor for atom (ParameterWrapper
                    or ParameterProxy). Note that the Bij and Bji parameters
                    are the same. (Bij = 8*pi**2*Uij)
    Biso        --  Isotropic ADP (ParameterWrapper).
    
    """

    def __init__(self, atom, name):
        """Initialize

        atom    --  A diffpy.Structure.Atom instance

        """
        ParameterSet.__init__(self, name)
        self.atom = atom
        a = atom
        # x, y, z, occupancy
        self.addParameter(ParameterWrapper("x", a, _xyzgetter(0),
            _xyzsetter(0)))
        self.addParameter(ParameterWrapper("y", a, _xyzgetter(1),
            _xyzsetter(1)))
        self.addParameter(ParameterWrapper("z", a, _xyzgetter(2),
            _xyzsetter(2)))
        occupancy = ParameterWrapper("occupancy", a, attr = "occupancy")
        self.addParameter(occupancy)
        self.addParameter(ParameterProxy("occ", occupancy))
        # U
        self.addParameter(ParameterWrapper("U11", a, attr = "U11"))
        self.addParameter(ParameterWrapper("U22", a, attr = "U22"))
        self.addParameter(ParameterWrapper("U33", a, attr = "U33"))
        U12 = ParameterWrapper("U12", a, attr = "U12")
        U21 = ParameterProxy("U21", U12)
        U13 = ParameterWrapper("U13", a, attr = "U13")
        U31 = ParameterProxy("U31", U13)
        U23 = ParameterWrapper("U23", a, attr = "U23")
        U32 = ParameterProxy("U32", U23)
        self.addParameter(U12)
        self.addParameter(U21)
        self.addParameter(U13)
        self.addParameter(U31)
        self.addParameter(U23)
        self.addParameter(U32)
        self.addParameter(ParameterWrapper("Uiso", a, attr = "Uisoequiv"))
        # B
        self.addParameter(ParameterWrapper("B11", a, attr = "B11"))
        self.addParameter(ParameterWrapper("B22", a, attr = "B22"))
        self.addParameter(ParameterWrapper("B33", a, attr = "B33"))
        B12 = ParameterWrapper("B12", a, attr = "B12")
        B21 = ParameterProxy("B21", B12)
        B13 = ParameterWrapper("B13", a, attr = "B13")
        B31 = ParameterProxy("B31", B13)
        B23 = ParameterWrapper("B23", a, attr = "B23")
        B32 = ParameterProxy("B32", B23)
        self.addParameter(B12)
        self.addParameter(B21)
        self.addParameter(B13)
        self.addParameter(B31)
        self.addParameter(B23)
        self.addParameter(B32)
        self.addParameter(ParameterWrapper("Biso", a, attr = "Bisoequiv"))

        # Other setup
        self.__repr__ = a.__repr__
        return

    def _getElem(self):
        return self.atom.element

    def _setElem(self, el):
        self.atom.element = el

    element = property(_getElem, _setElem, "type of atom")

# End class AtomParSet


def _latgetter(par):

    def f(lat):
        return getattr(lat, par)

    return f

def _latsetter(par):

    def f(lat, value):
        setattr(lat, par, value)
        lat.setLatPar()
        return

    return f


class LatticeParSet(ParameterSet):
    """A wrapper for diffpy.Structure.Lattice.

    This class derives from diffpy.srfit.fitbase.parameterset.ParameterSet. See
    this class for base attributes.

    Attributes
    lattice --  The diffpy.Structure.Lattice this is adapting
    name    --  Always "lattice"

    Managed Parameters:
    a, b, c, alpha, beta, gamma --  The lattice parameters (ParameterWrapper).
    
    """

    def __init__(self, lattice):
        """Initialize

        lattice --  A diffpy.Structure.Lattice instance

        """
        ParameterSet.__init__(self, "lattice")
        self.lattice = lattice
        l = lattice
        self.addParameter(ParameterWrapper("a", l, _latgetter("a"),
            _latsetter("a")))
        self.addParameter(ParameterWrapper("b", l, _latgetter("b"),
            _latsetter("b")))
        self.addParameter(ParameterWrapper("c", l, _latgetter("c"),
            _latsetter("c")))
        self.addParameter(ParameterWrapper("alpha", l, _latgetter("alpha"),
            _latsetter("alpha")))
        self.addParameter(ParameterWrapper("beta", l, _latgetter("beta"),
            _latsetter("beta")))
        self.addParameter(ParameterWrapper("gamma", l, _latgetter("gamma"),
            _latsetter("gamma")))

        # Other setup
        self.__repr__ = l.__repr__
        return

# End class LatticeParSet

class StructureParSet(BaseStructure):
    """A wrapper for diffpy.Structure.Structure.

    This class derives from diffpy.srfit.fitbase.parameterset.ParameterSet. See
    this class for base attributes.

    Attributes:
    atoms   --  The list of AtomParSets, provided for convenience.
    stru    --  The diffpy.Structure.Structure this is adapting

    Managed ParameterSets:
    lattice     --  The managed LatticeParSet
    <el><idx>   --  A managed AtomParSets. <el> is the atomic element and <idx>
                    is the index of that element in the structure, starting
                    from zero. Thus, for nickel in P1 symmetry, the managed
                    AtomParSets will be named "Ni0", "Ni1", "Ni2" and "Ni3".
    
    """

    def __init__(self, stru, name):
        """Initialize

        stru    --  A diffpy.Structure.Structure instance

        """
        ParameterSet.__init__(self, name)
        self.stru = stru
        self.addParameterSet(LatticeParSet(stru.lattice))
        self.atoms = []

        cdict = {}
        for a in stru:
            el = a.element
            i = cdict.get(el, 0)
            aname = "%s%i"%(el,i)
            cdict[el] = i+1
            atom = AtomParSet(a, aname)
            self.addParameterSet(atom)
            self.atoms.append(atom)

        # other setup
        self.__repr__ = stru.__repr__
        return

    def getLattice(self):
        """Get the ParameterSet containing the lattice Parameters."""
        return self.lattice

    @classmethod
    def canAdapt(self, stru):
        """Return whether the structure can be adapted by this class."""
        from diffpy.Structure import Structure
        return isinstance(stru, Structure)

    def getSites(self):
        """Get a list of ParameterSets that represents the sites.

        The site positions must be accessible from the list entries via the
        names "x", "y", and "z".

        """
        return self.atoms

    def getSpaceGroup(self):
        """Get the HM space group symbol for the structure."""
        return "P 1"


# End class StructureParSet

