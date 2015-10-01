"""SRW native API bending magnet example

Bending magnet emitting in x-ray region for a multi-electron emission
(by convolution)
"""
from __future__ import print_function
from srwlib import *
import numpy as np
from uti_plot import *
import time
import pytest

#: Set to True if you want output from the various stages
_DEBUG = True


#: Smallest number we can reasonably compare
_EPSILON = 1e-300


def main():
    wfr = test_bending_magnet_infrared_srw_native()
    mesh = deepcopy(wfr.mesh)
    arI1s = array('f', [0] * mesh.nx * mesh.ny)
    srwl.CalcIntFromElecField(arI1s, wfr, 6, 1, 3, mesh.eStart, 0, 0)
    import matplotlib.pyplot as plt
    dim_x = np.linspace(mesh.xStart, mesh.xFin, mesh.nx)
    dim_y = np.linspace(mesh.yStart, mesh.yFin, mesh.ny)
    intensity = np.array(arI1s).reshape((mesh.ny,mesh.nx))
    plt.pcolormesh(dim_x, dim_y, intensity)
    plt.title('Real space for infrared example')
    plt.colorbar()
    plt.show()


def run_bending_magnet_srw():
    t0_setting = time.time()
    B = 0.4
    LeffBM = 4.
    BM = SRWLMagFldM(B, 1, 'n', LeffBM)
    magFldCnt = SRWLMagFldC(
        [BM],
        array('d',[0]),
        array('d',[0]),
        array('d',[0]),
    )
    eBeam = SRWLPartBeam()
    eBeam.Iavg = 0.5
    eBeam.partStatMom1.x = 0.
    eBeam.partStatMom1.y = 0.
    eBeam.partStatMom1.z = 0.
    eBeam.partStatMom1.xp = 0.
    eBeam.partStatMom1.yp = 0.
    eBeam.partStatMom1.gamma = 3./0.51099890221e-03
    eBeam.arStatMom2[0] = 127.346e-06 ** 2
    eBeam.arStatMom2[1] = -10.85e-09
    eBeam.arStatMom2[2] = 92.3093e-06 ** 2
    eBeam.arStatMom2[3] = 13.4164e-06 ** 2
    eBeam.arStatMom2[4] = 0.0072e-09
    eBeam.arStatMom2[5] = 0.8022e-06 ** 2
    eBeam.arStatMom2[10] = 0.89e-03 ** 2
    wfr = SRWLWfr()
    wfr.allocate(1, 10, 10)
    distSrcLens = 5.
    wfr.mesh.zStart = distSrcLens
    wfr.mesh.eStart = 0.5 * 0.123984
    wfr.mesh.eFin = wfr.mesh.eStart
    horAng = 0.1
    wfr.mesh.xStart = -0.5 * horAng * distSrcLens
    wfr.mesh.xFin = 0.5 * horAng * distSrcLens
    verAng = 0.02
    wfr.mesh.yStart = -0.5 * verAng * distSrcLens
    wfr.mesh.yFin = 0.5 * verAng * distSrcLens
    wfr.partBeam = eBeam
    distLensImg = distSrcLens
    focLen = wfr.mesh.zStart * distLensImg / (distSrcLens + distLensImg)
    optLens = SRWLOptL(_Fx=focLen, _Fy=focLen)
    optDrift = SRWLOptD(distLensImg)
    propagParLens =  [1, 1, 1., 0, 0, 1., 2., 1., 2., 0, 0, 0]
    propagParDrift = [1, 1, 1., 0, 0, 1., 1., 1., 1., 0, 0, 0]
    optBL = SRWLOptC([optLens, optDrift], [propagParLens, propagParDrift])
    _debug('parameters done in {}s', round(time.time() - t0_setting))
    meth = 2
    relPrec = 0.01
    zStartInteg = 0
    zEndInteg = 0
    npTraj = 20000
    useTermin = 1
    sampFactNxNyForProp = 0.7
    arPrecSR = [meth, relPrec, zStartInteg, zEndInteg, npTraj, useTermin, sampFactNxNyForProp]
    _debug('Performing initial electric field calculation...')
    srwl.CalcElecFieldSR(wfr, 0, magFldCnt, arPrecSR)
    _debug('Extracting intensity from calculated electric field and saving it to file(s)')
    mesh0 = deepcopy(wfr.mesh)
    arI0 = array('f', [0] * mesh0.nx * mesh0.ny)
    srwl.CalcIntFromElecField(arI0, wfr, 6, 0, 3, mesh0.eStart, 0, 0)
    _debug('Simulating single-electron electric field wavefront propagation...')
    srwl.PropagElecField(wfr, optBL)
    return wfr


def test_bending_magnet_infrared_srw_native():
    wfr = run_bending_magnet_srw()
    checksum = np.sum( np.abs(wfr.arEx) ) + np.abs( np.sum(wfr.arEy) )
    _debug('checksum = {:f}', checksum)
    _assert(11845644288, checksum)
    return wfr


def _assert(expect, actual, expected_error=0.01):
    if _EPSILON > abs(expect):
        assert _EPSILON > abs(actual)
        return
    elif _EPSILON > abs(actual):
        raise AssertionError(
            'expect {} != {} actual'.format(expect, actual))
    assert expected_error > abs(expect/actual - 1)

def _assert_array(expect, actual):
    if np.shape(expect):
        for e, a in zip(expect, actual):
            _assert(e, a)
    else:
        _assert(expect, actual)


def _assert(expect, actual, expected_error=0.01):
    if _EPSILON > abs(expect):
        assert _EPSILON > abs(actual)
        return
    if _EPSILON <= abs(actual) and expected_error > abs(expect/actual - 1):
        return
    raise AssertionError(
        'expect {} != {} actual'.format(expect, actual))


def _debug(fmt, *args, **kwargs):
    """Format and print the message if _DEBUG

    Args:
        fmt (str): format string
    """
    if _DEBUG:
        print(str(args))


if __name__ == "__main__":
    main()
