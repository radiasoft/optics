"""SRW optics API bending magnet example

Bending magnet emitting in x-ray region for a multi-electron emission
(by convolution)
"""
import inspect
import matplotlib.pyplot as plt
import numpy as np
import time

from pykern import pkcollections

from code_drivers.SRW.SRW_beamline_component_setting import SRWBeamlineComponentSetting
from code_drivers.SRW.SRW_bending_magnet_setting import SRWBendingMagnetSetting
from code_drivers.SRW.SRW_driver import SRWDriver
from optics.beam.electron_beam_pencil import ElectronBeamPencil, ElectronBeam
from optics.beamline.beamline import Beamline
from optics.beamline.beamline_position import BeamlinePosition
from optics.beamline.optical_elements.image_plane import ImagePlane
from optics.beamline.optical_elements.lens.lens_ideal import LensIdeal
from optics.magnetic_structures.bending_magnet import BendingMagnet


#: Set to True if you want output from the various stages
_DEBUG = True


#: Smallest number we can reasonably compare
_EPSILON = 1e-300


def main():
    """test bending magnet and plot results"""
    res = test_bending_magnet_infrared()
    _debug('Calling plots with array shape: {}...', res.intensity.shape)
    plt.pcolormesh(res.dim_x, res.dim_y, res.intensity.transpose())
    plt.title('Real space for infrared example')
    plt.colorbar()
    plt.show()


def run_bending_magnet():
    electron_beam = ElectronBeamPencil(
        energy_in_GeV=3.0,
        energy_spread=0.89e-3,
        current=0.5,
    )
    bending_magnet = BendingMagnet(
        radius=25.01,
        magnetic_field=0.4,
        length=4.0,
    )
    srw_bending_magnet_setting = SRWBendingMagnetSetting()
    horizontal_angle = 0.1
    vertical_angle = 0.02
    energy = 0.5 * 0.123984
    srw_bending_magnet_setting.set_acceptance_angle(
        horizontal_angle=horizontal_angle,
        vertical_angle=vertical_angle,
    )
    bending_magnet.add_settings(srw_bending_magnet_setting)
    beamline  = Beamline()
    lens_focal_length = 2.5
    lens = LensIdeal(
        'focus lens',
        focal_x=lens_focal_length,
        focal_y=lens_focal_length,
    )
    lens_position = BeamlinePosition(2 * lens_focal_length)
    lens_setting = SRWBeamlineComponentSetting()
    lens_setting.set_auto_resize_before_propagation(1)
    lens_setting.set_auto_resize_after_propagation(1)
    lens_setting.set_auto_resize_relative_precision(1.)
    lens_setting.set_allow_semi_analytical_phase_treatment(0)
    lens_setting.set_resize_on_ft_side(0)
    lens_setting.set_resize_factor_horizontal(1.)
    lens_setting.set_resize_resolution_horizontal(2.)
    lens_setting.set_resize_factor_vertical(1.)
    lens_setting.set_resize_resolution_vertical(2.)
    lens.add_settings(lens_setting)
    beamline.attach_component_at(lens, lens_position)
    plane = ImagePlane('Image screen')
    plane_setting = SRWBeamlineComponentSetting()
    plane.add_settings(plane_setting)
    plane_position = BeamlinePosition(4*lens_focal_length)
    beamline.attach_component_at(plane, plane_position)
    driver = SRWDriver()
    wavefront = driver.calculate_radiation(
        electron_beam=electron_beam,
        magnetic_structure=bending_magnet,
        beamline=beamline,
        energy_min=energy,
        energy_max=energy,
    )
    res = driver.calculate_intensity(wavefront)
    res = pkcollections.OrderedMapping(
        dict(zip(('intensity', 'dim_x', 'dim_y'), res)))
    res.wavefront = wavefront
    return res


def test_bending_magnet_infrared():
    """Run the bending magnet example, check results, and plot output"""
    res = run_bending_magnet()
    flux = res.intensity.sum() \
        * (res.dim_x[1] - res.dim_x[0]) * (res.dim_y[1] - res.dim_y[0])
    _debug('Total flux = {:10.5e} photons/s/.1%bw', flux)
    _assert(2.40966e+08, flux)
    checksum = np.sum(np.abs(res.wavefront.arEx)) \
        + np.sum(np.abs(res.wavefront.arEy))
    _debug('checksum = {}', checksum)
    _assert(1.845644e10, checksum, 0.1)
    return res


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
        print(fmt.format(*args, **kwargs))


if __name__ == '__main__':
    main()
