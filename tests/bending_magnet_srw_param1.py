"""SRW declarative API bending magnet example

Bending magnet emitting in x-ray region for a multi-electron emission
(by convolution)
"""
from __future__ import absolute_import, division, print_function
from pykern.pkdebug import pkdc, pkdp

import copy
import itertools
import numpy as np
import srwlib as srw
import time

from pykern import pkarray
from pykern import pkcollections


#: Smallest number we can reasonably compare
_EPSILON = 1e-300


#: Default propagation parameters
_PROPAGATION = pkcollections.OrderedMapping(
    'auto_resize_before_propagation', True,
    'auto_resize_after_propagation', True,
    'auto_resize_relative_precision', 1.,
    'allow_semi_analytical_phase_treatment', False,
    'resize_on_fourier_side_using_fft', False,
    'horizontal_range_factor_when_resizing', 1.,
    'horizontal_resolution_factor_when_resizing', 1.,
    'vertical_range_factor_when_resizing', 1.,
    'vertical_resolution_factor_when_resizing', 1.,
    'unimplemented_0', 0,
    'unimplemented_1', 0,
    'unimplemented_2', 0,
)


_ELECTRON_BEAM = pkcollections.OrderedMapping(
    'average_current', .5,
    'moment_x', 0.,
    'moment_y', 0.,
    'moment_z', 0.,
    'moment_xp', 0.,
    'moment_yp', 0.,
    'moment_gamma', None,
    'moment_xx', 0.,
    'moment_xxp', 0.,
    'moment_xpxp', 0.,
    'moment_yy', 0.0,
    'eBeam.arStatMom2', 0.,
    'eBeam.arStatMom2', 0.,
    'moment_ypyp', 0.,
    'energy_spread_squared', 0.,
)

def main():
    wavefront = test_simulation()
    mesh = copy.deepcopy(wavefront.mesh)
    intensity = pkarray.new_float([0] * mesh.nx * mesh.ny)
    srw.srwl.CalcIntFromElecField(intensity, wavefront, 6, 1, 3, mesh.eStart, 0, 0)
    import matplotlib.pyplot as plt
    dim_x = np.linspace(mesh.xStart, mesh.xFin, mesh.nx)
    dim_y = np.linspace(mesh.yStart, mesh.yFin, mesh.ny)
    intensity = np.array(intensity).reshape((mesh.ny,mesh.nx))
    plt.pcolormesh(dim_x, dim_y, intensity)
    plt.title('Real space for infrared example')
    plt.colorbar()
    plt.show()


def simulate():
    t0_setting = time.time()
    B = 0.4
    LeffBM = 4.
    BM = srw.SRWLMagFldM(B, 1, 'n', LeffBM)
    magnetic_field_container = srw.SRWLMagFldC(
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
    wavefront = srw.SRWLWfr()
    wavefront.allocate(1, 10, 10)
    distSrcLens = 5.
    wavefront.mesh.zStart = distSrcLens
    wavefront.mesh.eStart = 0.5 * 0.123984
    wavefront.mesh.eFin = wavefront.mesh.eStart
    horAng = 0.1
    wavefront.mesh.xStart = -0.5 * horAng * distSrcLens
    wavefront.mesh.xFin = 0.5 * horAng * distSrcLens
    verAng = 0.02
    wavefront.mesh.yStart = -0.5 * verAng * distSrcLens
    wavefront.mesh.yFin = 0.5 * verAng * distSrcLens
    wavefront.partBeam = eBeam
    distLensImg = distSrcLens
    focLen = wavefront.mesh.zStart * distLensImg / (distSrcLens + distLensImg)
    optBL = _container(
        srw.SRWLOptL(_Fx=focLen, _Fy=focLen),
        dict(
            horizontal_resolution_factor_when_resizing=2.,
            vertical_resolution_factor_when_resizing=2.,
        ),
        srw.SRWLOptD(distLensImg),
        {},
    )
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
    srw.srwl.CalcElecFieldSR(wavefront, 0, magnetic_field_container, arPrecSR)
    pkdc('Extracting intensity from calculated electric field and saving it to file(s)')
    mesh0 = copy.deepcopy(wavefront.mesh)
    arI0 = pkarray.new_float([0] * mesh0.nx * mesh0.ny)
    srw.srwl.CalcIntFromElecField(arI0, wavefront, 6, 0, 3, mesh0.eStart, 0, 0)
    pkdc('Simulating single-electron electric field wavefront propagation...')
    srw.srwl.PropagElecField(wavefront, optBL)
    return wavefront


def test_simulation():
    wavefront = simulate()
    checksum = np.sum( np.abs(wavefront.arEx) ) + np.abs( np.sum(wavefront.arEy) )
    pkdc('checksum = {:f}', checksum)
    _assert(11845644288, checksum)
    return wavefront


def _assert(expect, actual, expected_error=0.01):
    if _EPSILON > abs(expect):
        assert _EPSILON > abs(actual)
        return
    if _EPSILON <= abs(actual) and expected_error > abs(expect/actual - 1):
        return
    raise AssertionError(
        'expect {} != {} actual'.format(expect, actual))


def _container(*args):
    """Create a container based

    Args:
        element (SRWLOptL, SRWLOptD, etc.): optical element
        propagation (dict): propagation param modifications
    """
    elements = []
    propagations = []
    for element, propagation in zip(args[0::2], args[1::2]):
        elements.append(element)
        propagations.append(_propagation(propagation))
    assert len(elements)
    return srw.SRWLOptC(elements, propagations)


def _propagation(values):
    merged = copy.deepcopy(_PROPAGATION)
    pkcollections.mapping_merge(merged, values)
    return pkcollections.map_values(
        merged,
        lambda v: int(v) if isinstance(v, bool) else v,
    )


if __name__ == "__main__":
    main()
