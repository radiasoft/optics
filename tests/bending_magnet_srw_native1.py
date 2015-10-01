"""SRW native API bending magnet example

Bending magnet emitting in x-ray region for a multi-electron emission
(by convolution)
"""
from __future__ import absolute_import, division, print_function
from pykern.pkdebug import pkdc, pkdp

import copy
import numpy as np
import srwlib as srw
import time

from pykern import pkarray
from pykern import pkcollections


#: Smallest number we can reasonably compare
_EPSILON = 1e-300


def main():
    wfr = test_simulation()
    mesh = copy.deepcopy(wfr.mesh)
    arI1s = pkarray.new_float([0] * mesh.nx * mesh.ny)
    srw.srwl.CalcIntFromElecField(arI1s, wfr, 6, 1, 3, mesh.eStart, 0, 0)
    import matplotlib.pyplot as plt
    dim_x = np.linspace(mesh.xStart, mesh.xFin, mesh.nx)
    dim_y = np.linspace(mesh.yStart, mesh.yFin, mesh.ny)
    intensity = np.array(arI1s).reshape((mesh.ny,mesh.nx))
    plt.pcolormesh(dim_x, dim_y, intensity)
    plt.title('Real space for infrared example')
    plt.colorbar()
    plt.show()


def simulate():
    t0_setting = time.time()
    B = 0.4
    LeffBM = 4.
    BM = srw.SRWLMagFldM(B, 1, 'n', LeffBM)
    magFldCnt = srw.SRWLMagFldC(
        [BM],
        pkarray.new_double([0]),
        pkarray.new_double([0]),
        pkarray.new_double([0]),
    )
    eBeam = srw.SRWLPartBeam()
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
    wfr = srw.SRWLWfr()
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
    optLens = srw.SRWLOptL(_Fx=focLen, _Fy=focLen)
    optDrift = srw.SRWLOptD(distLensImg)
    propagParLens =  [1, 1, 1., 0, 0, 1., 2., 1., 2., 0, 0, 0]
    propagParDrift = [1, 1, 1., 0, 0, 1., 1., 1., 1., 0, 0, 0]
    optBL = srw.SRWLOptC([optLens, optDrift], [propagParLens, propagParDrift])
    pkdc('parameters done in {}s', round(time.time() - t0_setting))
    meth = 2
    relPrec = 0.01
    zStartInteg = 0
    zEndInteg = 0
    npTraj = 20000
    useTermin = 1
    sampFactNxNyForProp = 0.7
    arPrecSR = [meth, relPrec, zStartInteg, zEndInteg, npTraj, useTermin, sampFactNxNyForProp]
    pkdc('Performing initial electric field calculation...')
    srw.srwl.CalcElecFieldSR(wfr, 0, magFldCnt, arPrecSR)
    pkdc('Extracting intensity from calculated electric field and saving it to file(s)')
    mesh0 = copy.deepcopy(wfr.mesh)
    arI0 = pkarray.new_float([0] * mesh0.nx * mesh0.ny)
    srw.srwl.CalcIntFromElecField(arI0, wfr, 6, 0, 3, mesh0.eStart, 0, 0)
    pkdc('Simulating single-electron electric field wavefront propagation...')
    srw.srwl.PropagElecField(wfr, optBL)
    return wfr


def test_simulation():
    wfr = simulate()
    checksum = np.sum( np.abs(wfr.arEx) ) + np.abs( np.sum(wfr.arEy) )
    pkdc('checksum = {:f}', checksum)
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


def _assert(expect, actual, expected_error=0.01):
    if _EPSILON > abs(expect):
        assert _EPSILON > abs(actual)
        return
    if _EPSILON <= abs(actual) and expected_error > abs(expect/actual - 1):
        return
    raise AssertionError(
        'expect {} != {} actual'.format(expect, actual))


if __name__ == "__main__":
    main()
