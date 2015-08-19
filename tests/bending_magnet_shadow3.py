"""
Example of a bending magnet emitting in X-ray region for multiple electron emission
"""

import os
import numpy as np
import inspect

# Import elements from common Glossary
from optics.beam.electron_beam_pencil import ElectronBeamPencil, ElectronBeam
from optics.magnetic_structures.bending_magnet import BendingMagnet

from optics.beamline.optical_elements.lens.lens_ideal import LensIdeal
from optics.beamline.optical_elements.image_plane import ImagePlane

from optics.beamline.beamline import Beamline
from optics.beamline.beamline_position import BeamlinePosition

#import Shadow driver and particular settings of the glossary elements used
from code_drivers.shadow.driver.shadow_driver import ShadowDriver
from code_drivers.shadow.sources.shadow_bending_magnet import ShadowBendingMagnetSetting


def run_bending_magnet_shadow3(example_index):#  example_index=0 is infrared example, example_index=1 is xrays example
    ###################################################################################################
    # Main idea: abstract definition of the setting (electron beam, radiation source, beamline)
    # We want to put everything in generic classes that is independent of a specific implementation.
    # These are basically the information a scientist would need to physically build the beamline.
    #
    # Then, we need extra information/settings to perform a calculation. And the extra settings
    # vary for different programs. We provide these extra information by attaching program depended
    # "settings".
    ###################################################################################################




    # Specify to use Shadow
    driver = ShadowDriver()

    #
    # 1) define first the electron beam
    #

    if example_index == 0:
        energy_in_GeV = 3.0
        electron_beam = ElectronBeamPencil(energy_in_GeV=energy_in_GeV,energy_spread=0.89e-3,current=0.5)
        # electron_beam = ElectronBeam(energy_in_GeV=energy_in_GeV,
        #                             energy_spread=0.89e-03,
        #                             current=0.5,
        #                             electrons_per_bunch=500,
        #                             moment_xx   = (127.346e-6)**2 ,
        #                             moment_xxp  = 0.            ,
        #                             moment_xpxp = 100*(91.88e-6)**2,
        #                             moment_yy   = (92.3093e-6)**2 ,
        #                             moment_yyp  = 0             ,
        #                             moment_ypyp = 100*(7.94e-6)**2  )

    else:
        energy_in_GeV = 6.0
        #electron_beam = ElectronBeamPencil(energy_in_GeV=energy_in_GeV,energy_spread=0.89e-3,current=0.2)
        electron_beam = ElectronBeam(energy_in_GeV=energy_in_GeV,
                                    energy_spread=0.89e-03,
                                    current=0.2,
                                    electrons_per_bunch=500,
                                    moment_xx   = (77.9e-06)**2 ,
                                    moment_xxp  = 0.            ,
                                    moment_xpxp = (110.9e-06)**2,
                                    moment_yy   = (12.9e-06)**2 ,
                                    moment_yyp  = 0             ,
                                    moment_ypyp = (0.5e-06)**2  )


    #
    # 2) define the magnetic structure
    #


    if example_index == 0:
        fan_divergence = 0.1
        magnetic_field = 0.4

    else:
        fan_divergence = 0.004
        magnetic_field = 0.8

    radius = 3.334728 * energy_in_GeV / magnetic_field

    bending_magnet = BendingMagnet(radius=radius,magnetic_field=magnetic_field,length=radius*fan_divergence)

    # Attach SHADOW bending magnet settings.
    shadow_bending_magnet_settings = ShadowBendingMagnetSetting()

    if example_index == 0:
        shadow_bending_magnet_settings._number_of_rays = 5000
        shadow_bending_magnet_settings._calculation_mode = 1
        shadow_bending_magnet_settings._max_vertical_half_divergence_from = 0.01
        shadow_bending_magnet_settings._max_vertical_half_divergence_to = 0.01
    else:
        shadow_bending_magnet_settings._number_of_rays = 26000
        calculation_mode = 1 # exact calculation
        if calculation_mode == 1: #for exact calculations, the max divergence has to be set to reasonable values
            shadow_bending_magnet_settings._calculation_mode = 1
            shadow_bending_magnet_settings._max_vertical_half_divergence_from = 0.04
            shadow_bending_magnet_settings._max_vertical_half_divergence_to = 0.04
        else: #for pre-computer calculations, the max divergence can be set to a very large value (1rad~infinity)
            shadow_bending_magnet_settings._calculation_mode = 0
            shadow_bending_magnet_settings._max_vertical_half_divergence_from = 1.0
            shadow_bending_magnet_settings._max_vertical_half_divergence_to = 1.0

    bending_magnet.add_settings(shadow_bending_magnet_settings)

    #
    # 3) define beamline containing the optical elements
    #    In this case, create a beamline that only has one lens attached plus an image (detector) plane
    #

    #
    beamline  = Beamline()

    if example_index == 0:
        lens_focal_length = 2.5
    else:
        lens_focal_length = 12.5


    # First create the lens.
    lens=LensIdeal("focus lens",
                   focal_x=lens_focal_length,
                   focal_y=lens_focal_length)
    # Specify the position of the lens (could set extra parameters for: off-axis and inclination)
    lens_position = BeamlinePosition(2*lens_focal_length)

    # Attach the component at its position to the beamline.
    beamline.attach_component_at(lens, lens_position)

    # Attach a screen/image plane.
    plane_position = BeamlinePosition(4*lens_focal_length)
    beamline.attach_component_at(ImagePlane("Image screen"), plane_position)

    #
    #  Print a summary of the elements used
    #
    components = [electron_beam,bending_magnet,lens]
    print("===========================================================================================================")
    for component_index,component in enumerate(components):
        tmp = component.to_dictionary()
        print("Component index %d:"%component_index,inspect.getmodule(component))
        for i,var in enumerate(tmp):
            print("   %20s = %10.5e %5s  %s"%(var,tmp[var][0],tmp[var][1],tmp[var][2]))
        print("===========================================================================================================")


    #
    #  Calculate the radiation (i.e., run the codes). It returns a native Shadow.Beam()
    #


    if example_index == 0:
        energy = 0.5*0.123984
    else:
        energy = 15000.0


    shadow_beam = driver.calculate_radiation(electron_beam=electron_beam,
                                             magnetic_structure=bending_magnet,
                                             beamline=beamline,
                                             energy_min = energy,
                                             energy_max = energy)
    #shadow_beam._beam.write("tmp.01")

    #
    # extract and plot the intensity
    #
    intensity,dim_x,dim_y = driver.calculate_intensity(shadow_beam)

    #
    # clean temporary shadow files
    #

    #
    if example_index == 0:
        os.remove("SPER00000")
        os.remove("FLUX")
        os.remove("SPAR00000")
        os.remove("STOT00000")
    else:
        os.remove("SPER15000")
        os.remove("FLUX")
        os.remove("SPAR15000")
        os.remove("STOT15000")

    return shadow_beam, dim_x, dim_y, intensity


def test_bending_magnet_infrared_shadow3():
    shadow_beam, dim_x, dim_y, intensity = run_bending_magnet_shadow3(0)
    # Do some tests
    # Shadow results are random. But test at least that it really run
    #     assert shadow_beam._beam.rays.shape == (5000, 18), "Test shadow beam shape"
    #     assert shadow_beam._beam.rays.shape == (5000, 18), "Test shadow beam shape"
    assert shadow_beam._beam.rays.shape == (5000, 18), "Test shadow beam shape"
    assert np.sum(np.abs(shadow_beam._beam.rays[:,7])) > 1, "Test E field not zero"
    return shadow_beam, dim_x, dim_y, intensity

def test_bending_magnet_xrays_shadow3():
    shadow_beam, dim_x, dim_y, intensity = run_bending_magnet_shadow3(1)
    # Do some tests
    # Shadow results are random. But test at least that it really run
    #     assert shadow_beam._beam.rays.shape == (5000, 18), "Test shadow beam shape"
    assert shadow_beam._beam.rays.shape == (26000, 18), "Test shadow beam shape"
    assert np.sum(np.abs(shadow_beam._beam.rays[:,7])) > 1, "Test E field not zero"
    return shadow_beam, dim_x, dim_y, intensity

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    #
    # infrared example
    #
    shadow_beam, dim_x, dim_y, intensity = test_bending_magnet_infrared_shadow3()
    # Plot
    plt.pcolormesh(dim_x,dim_y,intensity.transpose())
    plt.title("Real space for infrared example")
    plt.colorbar()
    plt.show()

    #
    # xrays example
    #
    shadow_beam, dim_x, dim_y, intensity = test_bending_magnet_xrays_shadow3()
    # Plot
    plt.pcolormesh(dim_x,dim_y,intensity.transpose())
    plt.title("Real space for xrays example")
    plt.colorbar()
    plt.show()