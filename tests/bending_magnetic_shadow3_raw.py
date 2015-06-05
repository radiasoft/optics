#
# Python script to run shadow3. Created automatically with mk_script.py.
#
import Shadow
import pytest
import os

def bending_magnet_shadow3_raw_run():

    # write (1) or not (0) SHADOW files start.xx end.xx star.xx
    iwrite = 0

    #
    # initialize shadow3 source (oe0) and beam
    #
    beam = Shadow.Beam()
    oe0 = Shadow.Source()
    oe1 = Shadow.OE()

    #
    #define variables (see source.nml and oe.nml for doc)
    #

    oe0.BENER = 3.0
    oe0.FDISTR = 6
    oe0.FSOURCE_DEPTH = 4
    oe0.F_COLOR = 3
    oe0.F_PHOT = 0
    oe0.HDIV1 = 0.0500000007
    oe0.HDIV2 = 0.0500000007
    oe0.ISTAR1 = 567656
    oe0.NCOL = 0
    oe0.N_COLOR = 0
    oe0.PH1 = 0.0599999987
    oe0.PH2 = 0.0610000007
    oe0.POL_DEG = 0.0
    oe0.R_ALADDIN = -2501.0459
    oe0.R_MAGNET = 25.0104599
    oe0.SIGDIX = 0.0
    oe0.SIGDIZ = 0.0
    oe0.SIGMAX = 0.0
    oe0.SIGMAY = 0.0
    oe0.SIGMAZ = 0.0
    oe0.VDIV1 = 0.00999999978
    oe0.VDIV2 = 0.00999999978
    oe0.WXSOU = 0.0
    oe0.WYSOU = 0.0
    oe0.WZSOU = 0.0

    oe1.FMIRR = 2
    oe1.HOLO_W = 4879.85986
    oe1.NCOL = 0
    oe1.R_LAMBDA = 5000.0
    oe1.T_IMAGE = 500.0
    oe1.T_INCIDENCE = 20.0
    oe1.T_REFLECTION = 20.0
    oe1.T_SOURCE = 500.0



    #Run SHADOW to create the source

    if iwrite:
        oe0.write("start_py.00")

    beam.genSource(oe0)

    if iwrite:
        oe0.write("end_py.00")
        beam.write("begin.dat")


    #
    #run optical element 1
    #
    if iwrite:
        oe1.write("start_py.01")
    beam.traceOE(oe1,1)
    if iwrite:
        oe1.write("end_py.01")
        beam.write("star.01")



    return beam

def test_shadow3_raw():
    beam = bending_magnet_shadow3_raw_run()

    Shadow.ShadowTools.plotxy(beam,1,3,nbins=101,title="Real space")
    Shadow.ShadowTools.plotxy(beam,1,4,nbins=101,title="Phase space X")
    Shadow.ShadowTools.plotxy(beam,3,6,nbins=101,title="Phase space Z")

    os.remove("effic.01")
    os.remove("mirr.01")
    os.remove("rmir.01")
    os.remove("SPER00000")
    os.remove("optax.01")
    os.remove("star.01")
    os.remove("FLUX")
    os.remove("SPAR00000")
    os.remove("STOT00000")



    