#!/usr/bin/env python
########################################################################
#
# diffpy.srfit      by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2009 The Trustees of Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE_DANSE.txt for license information.
#
########################################################################

"""Example of extracting information from multiple data sets simultaneously.

This example builds on npintensitygenerator.py, and uses IntensityGenerator
from that example to build a recipe that simultaneously refines two data sets
generated from the same structure.

Instructions

Run the example and then read through the 'makeRecipe' code. You will see how
to refine a single structure to two data sets.

Extensions

- In 'makeRecipe' the fit contributions are identically configured except for
  the profile. Factor out that configuration code and apply it in the
  'makeRecipe' method. This will reduce the amount of code required to get the
  job done, make it clearer what is being done and therefore reduce potential
  mistakes in the code. This encapsulation of configuration workflow is the
  first step towards writing a user interface.
"""

import numpy

from diffpy.srfit.fitbase import FitContribution, FitRecipe, Profile, FitResults
from npintensity import IntensityGenerator
from npintensity import makeData

from gaussianrecipe import scipyOptimize

####### Example Code

def makeRecipe(strufile, datname1, datname2):
    """Create a recipe that uses the IntensityGenerator.

    We will create two FitContributions that use the IntensityGenerator from
    npintensitygenerator.py and associate each of these with a Profile, and use
    this to define a FitRecipe.

    Both simulated data sets come from the same structure. We're going to make
    two FitContributions that are identical, except for the profile that is
    held in each. We're going to assure that the structures are identical by
    using the same DiffpyStructureParSet (which is generated by the
    IntensityGenerator when we load the structure) in both generators.

    """

    ## The Profiles
    # Create two Profiles for the two FitContributions.
    profile1 = Profile()
    profile2 = Profile()

    # Load data into the Profiles
    profile1.loadtxt(datname1)
    x, y, u = profile2.loadtxt(datname2)

    ## The ProfileGenerators
    # Create two IntensityGenerators named "I". There will not be a name
    # conflict, since the name is only meaningful within the FitContribution
    # that holds the ProfileGenerator.  Load the structure into one and make
    # sure that the second ProfileGenerator is using the same
    # DiffyStructureParSet.  This will assure that both ProfileGenerators are
    # using the exact same Parameters, and underlying Structure object in the
    # calculation of the profile.
    generator1 = IntensityGenerator("I")
    generator1.setStructure(strufile)
    generator2 = IntensityGenerator("I")
    generator2.addParameterSet(generator1.phase)

    ## The FitContributions
    # Create the FitContributions.
    contribution1 = FitContribution("bucky1")
    contribution1.addProfileGenerator(generator1)
    contribution1.setProfile(profile1, xname = "q")
    contribution2 = FitContribution("bucky2")
    contribution2.addProfileGenerator(generator2)
    contribution2.setProfile(profile2, xname = "q")

    # Now we're ready to define the fitting equation for each FitContribution.
    # The functions registered below will be independent, even though they take
    # the same form and use the same Parameter names.  By default, Parameters
    # in different contributions are different Parameters even if they have the
    # same names.  FitContributions are isolated namespaces than only share
    # information if you tell them to by using addParameter or addParameterSet.
    bkgdstr = "b0 + b1*q + b2*q**2 + b3*q**3 + b4*q**4 + b5*q**5 + b6*q**6 +\
               b7*q**7 +b8*q**8 + b9*q**9"

    contribution1.registerStringFunction(bkgdstr, "bkgd")
    contribution2.registerStringFunction(bkgdstr, "bkgd")

    # We will create the broadening function by registering a python function.
    pi = numpy.pi
    exp = numpy.exp
    def gaussian(q, q0, width):
        return 1/(2*pi*width**2)**0.5 * exp(-0.5 * ((q-q0)/width)**2)

    contribution1.registerFunction(gaussian)
    contribution2.registerFunction(gaussian)
    # Center the gaussian
    contribution1.q0.value = x[len(x) // 2]
    contribution2.q0.value = x[len(x) // 2]

    # Now we can incorporate the scale and bkgd into our calculation. We also
    # convolve the signal with the gaussian to broaden it.
    contribution1.setEquation("scale * convolve(I, gaussian) + bkgd")
    contribution2.setEquation("scale * convolve(I, gaussian) + bkgd")

    # Make a FitRecipe and associate the FitContributions.
    recipe = FitRecipe()
    recipe.addContribution(contribution1)
    recipe.addContribution(contribution2)

    # Specify which Parameters we want to refine. We want to refine the
    # background that we just defined in the FitContributions. We have to do
    # this separately for each FitContribution. We tag the variables so it is
    # easy to retrieve the background variables.
    recipe.addVar(contribution1.b0, 0, name = "b1_0", tag = "bcoeffs1")
    recipe.addVar(contribution1.b1, 0, name = "b1_1", tag = "bcoeffs1")
    recipe.addVar(contribution1.b2, 0, name = "b1_2", tag = "bcoeffs1")
    recipe.addVar(contribution1.b3, 0, name = "b1_3", tag = "bcoeffs1")
    recipe.addVar(contribution1.b4, 0, name = "b1_4", tag = "bcoeffs1")
    recipe.addVar(contribution1.b5, 0, name = "b1_5", tag = "bcoeffs1")
    recipe.addVar(contribution1.b6, 0, name = "b1_6", tag = "bcoeffs1")
    recipe.addVar(contribution1.b7, 0, name = "b1_7", tag = "bcoeffs1")
    recipe.addVar(contribution1.b8, 0, name = "b1_8", tag = "bcoeffs1")
    recipe.addVar(contribution1.b9, 0, name = "b1_9", tag = "bcoeffs1")
    recipe.addVar(contribution2.b0, 0, name = "b2_0", tag = "bcoeffs2")
    recipe.addVar(contribution2.b1, 0, name = "b2_1", tag = "bcoeffs2")
    recipe.addVar(contribution2.b2, 0, name = "b2_2", tag = "bcoeffs2")
    recipe.addVar(contribution2.b3, 0, name = "b2_3", tag = "bcoeffs2")
    recipe.addVar(contribution2.b4, 0, name = "b2_4", tag = "bcoeffs2")
    recipe.addVar(contribution2.b5, 0, name = "b2_5", tag = "bcoeffs2")
    recipe.addVar(contribution2.b6, 0, name = "b2_6", tag = "bcoeffs2")
    recipe.addVar(contribution2.b7, 0, name = "b2_7", tag = "bcoeffs2")
    recipe.addVar(contribution2.b8, 0, name = "b2_8", tag = "bcoeffs2")
    recipe.addVar(contribution2.b9, 0, name = "b2_9", tag = "bcoeffs2")

    # We also want to adjust the scale and the convolution width
    recipe.addVar(contribution1.scale, 1, name = "scale1")
    recipe.addVar(contribution1.width, 0.1, name = "width1")
    recipe.addVar(contribution2.scale, 1, name = "scale2")
    recipe.addVar(contribution2.width, 0.1, name = "width2")

    # We can also refine structural parameters. We only have to do this once,
    # since each generator holds the same DiffpyStructureParSet.
    phase = generator1.phase
    lattice = phase.getLattice()
    a = recipe.addVar(lattice.a)
    # We want to allow for isotropic expansion, so we'll make constraints for
    # that.
    recipe.constrain(lattice.b, a)
    recipe.constrain(lattice.c, a)
    # We want to refine the thermal parameters as well. We will add a new
    # variable that we call "Uiso" and constrain the atomic Uiso values to
    # this. Note that we don't give Uiso an initial value. The initial value
    # will be inferred from the subsequent constraints.
    Uiso = recipe.newVar("Uiso")
    for atom in phase.getScatterers():
        recipe.constrain(atom.Uiso, Uiso)

    # Give the recipe away so it can be used!
    return recipe

def plotResults(recipe):
    """Plot the results contained within a refined FitRecipe."""

    # plotting song and dance
    q = recipe.bucky1.profile.x

    # Plot this for fun.
    I1 = recipe.bucky1.profile.y
    Icalc1 = recipe.bucky1.profile.ycalc
    bkgd1 = recipe.bucky1.evaluateEquation("bkgd")
    diff1 = I1 - Icalc1
    I2 = recipe.bucky2.profile.y
    Icalc2 = recipe.bucky2.profile.ycalc
    bkgd2 = recipe.bucky2.evaluateEquation("bkgd")
    diff2 = I2 - Icalc2
    offset = 1.2 * max(I2) * numpy.ones_like(I2)
    I1 += offset
    Icalc1 += offset
    bkgd1 += offset
    diff1 += offset

    import pylab
    pylab.subplot(2, 1, 1)
    pylab.plot(q,I1,'bo',label="I1(Q) Data")
    pylab.plot(q,Icalc1,'r-',label="I1(Q) Fit")
    pylab.plot(q,diff1,'g-',label="I1(Q) diff")
    pylab.plot(q,bkgd1,'c-',label="Bkgd1 Fit")
    pylab.legend(loc=1)

    pylab.subplot(2, 1, 2)
    pylab.plot(q,I2,'bo',label="I2(Q) Data")
    pylab.plot(q,Icalc2,'r-',label="I2(Q) Fit")
    pylab.plot(q,diff2,'g-',label="I2(Q) diff")
    pylab.plot(q,bkgd2,'c-',label="Bkgd2 Fit")
    pylab.xlabel("$Q (\AA^{-1})$")
    pylab.ylabel("Intensity (arb. units)")
    pylab.legend(loc=1)

    pylab.show()
    return

def main():

    # Make two different data sets, each from the same structure, but with
    # different scale, noise, broadening and background.
    strufile = "data/C60.stru"
    q = numpy.arange(1, 20, 0.05)
    makeData(strufile, q, "C60_1.iq", 8.1, 101.68, 0.008, 0.12, 2, 0.01)
    makeData(strufile, q, "C60_2.iq", 3.2, 101.68, 0.02, 0.003, 0, 1)

    # Make the recipe
    recipe = makeRecipe(strufile, "C60_1.iq", "C60_2.iq")

    # Optimize
    # Since the backgrounds have a large effect on the profile, we will refine
    # them first, but do so separately.
    # To refine the background from the first contribution, we will fix
    # all other parameters and give the second contribution no weight in the
    # fit.
    recipe.fix("all")
    recipe.free("bcoeffs1")
    recipe.setWeight(recipe.bucky2, 0)
    scipyOptimize(recipe)
    # Now do the same for the second background
    recipe.fix("all")
    recipe.free("bcoeffs1")
    recipe.setWeight(recipe.bucky2, 1)
    recipe.setWeight(recipe.bucky1, 0)
    scipyOptimize(recipe)
    # Now refine everything with the structure parameters included
    recipe.free("all")
    recipe.setWeight(recipe.bucky1, 1)
    scipyOptimize(recipe)

    # Generate and print the FitResults
    res = FitResults(recipe)
    res.printResults()

    # Plot!
    plotResults(recipe)

    return

if __name__ == "__main__":

    main()

# End of file
