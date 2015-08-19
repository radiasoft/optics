"""
Example of a bending magnet emitting in x-ray region for a multi-electron emission (by convolution)
"""
import numpy as np
import inspect

# Import elements from common Glossary
from optics.beam.electron_beam_pencil import ElectronBeamPencil, ElectronBeam
from optics.magnetic_structures.bending_magnet import BendingMagnet

from optics.beamline.optical_elements.lens.lens_ideal import LensIdeal
from optics.beamline.optical_elements.image_plane import ImagePlane

from optics.beamline.beamline import Beamline
from optics.beamline.beamline_position import BeamlinePosition

#import SRW driver and particular settings of the glossary elements used
from code_drivers.SRW.SRW_driver import SRWDriver
from code_drivers.SRW.SRW_bending_magnet_setting import SRWBendingMagnetSetting
from code_drivers.SRW.SRW_beamline_component_setting import SRWBeamlineComponentSetting





def run_bending_magnet_srw(example_index): #  example_index=0 is infrared example, example_index=1 is xrays example
    ###################################################################################################
    # Main idea: abstract definition of the setting (electron beam, radiation source, beamline)
    # We want to put everything in generic classes that is independent of a specific implementation.
    # These are basically the information a scientist would need to physically build the beamline.
    #
    # Then, we need extra information/settings to perform a calculation. And the extra settings
    # vary for different programs. We provide these extra information by attaching program depended
    # "settings".
    ###################################################################################################

    #
    # 1) define first the electron beam
    #

    if example_index == 0:
        electron_beam = ElectronBeamPencil(energy_in_GeV=3.0,energy_spread=0.89e-3,current=0.5)
        # electron_beam = ElectronBeam(energy_in_GeV=3.0,
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
        #electron_beam = ElectronBeamPencil(energy_in_GeV=6.0,energy_spread=0.89e-3,current=0.2)
        electron_beam = ElectronBeam(energy_in_GeV=6.0,
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
        #bending_magnet = BendingMagnet(radius=2.25,magnetic_field=0.4,length=4.0)
        bending_magnet = BendingMagnet(radius=25.01,magnetic_field=0.4,length=4.0)
    else:
        bending_magnet = BendingMagnet(radius=23.2655,magnetic_field=0.86,length=0.5)


    # Attach SRW bending magnet settings.
    #TODO: angular acceptance is used to define screen size.
    # NOTE: Maybe angular acceptance is generic and should move to BendingMagnet or Source class??

    srw_bending_magnet_setting = SRWBendingMagnetSetting()

    if example_index == 0:
        horizontal_angle = 0.1
        vertical_angle = 0.02
        energy = 0.5*0.123984
    else:
        horizontal_angle = 1e-3
        vertical_angle = 0.4e-3
        energy = 15000.0
        srw_bending_magnet_setting.set_relPrec(0.003)
        srw_bending_magnet_setting.set_sampFactNxNyForProp(0.0035)

    srw_bending_magnet_setting.set_acceptance_angle(horizontal_angle=horizontal_angle,
                                                    vertical_angle=vertical_angle)

    bending_magnet.add_settings(srw_bending_magnet_setting)


    #
    # 3) define beamline containing the optical elements
    #    In this case, create a beamline that only has one lens attached plus an image (detector) plane
    #

    #
    beamline  = Beamline()

    # First create the lens.

    if example_index == 0:
        lens_focal_length = 2.5
    else:
        lens_focal_length = 12.5

    lens = LensIdeal("focus lens",
                   focal_x=lens_focal_length,
                   focal_y=lens_focal_length)

    # Specify the position of the lens (could set extra parameters for: off-axis and inclination)
    # lens_position=p  verifies lens equation (1/F = 1/p + 1/q, and p=q for 1:1 magnification)
    lens_position = BeamlinePosition(2*lens_focal_length)

    # Set settings for SRW.
    # These are settings that depend on the "driver" to use.
    # If no special settings are set the driver will use its default settings.

    lens_setting = SRWBeamlineComponentSetting()

    if example_index == 0:
        #for SRW experts:
        #lens_setting.from_list([1, 1, 1., 0, 0, 1., 2., 1., 2., 0, 0, 0])

        lens_setting.set_auto_resize_before_propagation(1)         #[0]: Auto-Resize (1) or not (0) Before propagation
        lens_setting.set_auto_resize_after_propagation(1)          #[1]: Auto-Resize (1) or not (0) After propagation
        lens_setting.set_auto_resize_relative_precision(1.)        #[2]: Relative Precision for propagation with Auto-Resizing (1. is nominal)
        lens_setting.set_allow_semi_analytical_phase_treatment(0)  #[3]: Allow (1) or not (0) for semi-analytical treatment of the quadratic (leading) phase terms at the propagation
        lens_setting.set_resize_on_ft_side(0)                      #[4]: Do any Resizing on Fourier side, using FFT, (1) or not (0)
        lens_setting.set_resize_factor_horizontal(1.)              #[5]: Horizontal Range modification factor at Resizing (1. means no modification)
        lens_setting.set_resize_resolution_horizontal(2.)          #[6]: Horizontal Resolution modification factor at Resizing
        lens_setting.set_resize_factor_vertical(1.)                #[7]: Vertical Range modification factor at Resizing
        lens_setting.set_resize_resolution_vertical(2.)            #[8]: Vertical Resolution modification factor at Resizing
    else:
        #lens_setting.from_list([0, 0, 1., 0, 0, 1., 5., 1., 8., 0, 0, 0])
        lens_setting.set_auto_resize_before_propagation(0)
        lens_setting.set_auto_resize_after_propagation(0)
        lens_setting.set_auto_resize_relative_precision(1.)
        lens_setting.set_allow_semi_analytical_phase_treatment(0)
        lens_setting.set_resize_on_ft_side(0)
        lens_setting.set_resize_factor_horizontal(1.)
        lens_setting.set_resize_resolution_horizontal(5.)
        lens_setting.set_resize_factor_vertical(1.)
        lens_setting.set_resize_resolution_vertical(8.)

    lens.add_settings(lens_setting)

    # We could also _simultaneously_ add settings for shadow here:
    # lens_setting = ShadowBeamlineComponentSetting()
    # lens_setting.setSOMETHING(..)
    # lens.addSettings(lens_setting)
    # The lens would be configured _simultaneously_ for SRW and SHADOW.

    # Attach the component at its position to the beamline.
    beamline.attach_component_at(lens, lens_position)


    # Second create the image plane.

    plane = ImagePlane("Image screen")


    plane_setting = SRWBeamlineComponentSetting()

    if example_index == 0:
        pass #these are default values, so no need to set
        #plane_setting.from_list([1, 1, 1., 0, 0, 1., 1., 1., 1., 0, 0, 0])
        #plane_setting.set_auto_resize_before_propagation(0)
        #plane_setting.set_auto_resize_after_propagation(0)
        #plane_setting.set_auto_resize_relative_precision(1.)
        #plane_setting.set_allow_semi_analytical_phase_treatment(0)
        #plane_setting.set_resize_on_ft_side(0)
        #plane_setting.set_resize_factor_horizontal(1.)
        #plane_setting.set_resize_resolution_horizontal(1.)
        #plane_setting.set_resize_factor_vertical(1.)
        #plane_setting.set_resize_resolution_vertical(1.)
    else:
        #define non-default settings for the propagation in the drift space
        #note that although in SRW the driftSpace is a component, in the present beamline
        #definition it is not necessary to be defined, as it is automatically added by the
        #driver. However, we set here the settings of the drift space that is inserted upstream
        #of the "plane" element
        drift_space_settings = SRWBeamlineComponentSetting()
        drift_space_settings.from_list([0, 0, 1., 1, 0, 1., 1., 1., 1., 0, 0, 0])

        plane_setting.set_drift_space_settings(drift_space_settings)

        #plane_setting.from_list([0, 0, 1., 0, 0, 4., 1.,1.5, 1., 0, 0, 0])
        plane_setting.set_auto_resize_before_propagation(0)
        plane_setting.set_auto_resize_after_propagation(0)
        plane_setting.set_auto_resize_relative_precision(1.)
        plane_setting.set_allow_semi_analytical_phase_treatment(0)
        plane_setting.set_resize_on_ft_side(0)
        plane_setting.set_resize_factor_horizontal(4.)
        plane_setting.set_resize_resolution_horizontal(1.)
        plane_setting.set_resize_factor_vertical(1.5)
        plane_setting.set_resize_resolution_vertical(1.)



    # Attach a screen/image plane.
    # Absolute position = distance_source_lens + distance_lens_plane =
    #                       2*lens_focal_length + 2*lens_focal_lengh = 4*lens_focal_length
    plane.add_settings(plane_setting)
    plane_position = BeamlinePosition(4*lens_focal_length)


    beamline.attach_component_at(plane, plane_position)


    #
    #  Print a summary of the elements used
    #
    components = [electron_beam,bending_magnet,lens]
    print("===========================================================================================================")
    for component_index,component in enumerate(components):
        tmp = component.to_dictionary()
        #tmp = electron_beam.to_dictionary()

        print("Component index %d:"%component_index,inspect.getmodule(component))
        for i,var in enumerate(tmp):
            print("   %20s = %10.5f %5s  %s"%(var,tmp[var][0],tmp[var][1],tmp[var][2]))
        print("===========================================================================================================")


    #
    #  Calculate the radiation (i.e., run the codes). It returns a native SRWLWfr()
    #

    # Specify to use SRW.
    driver = SRWDriver()

    srw_wavefront = driver.calculate_radiation(electron_beam=electron_beam,
                                               magnetic_structure=bending_magnet,
                                               beamline=beamline,
                                               energy_min=energy,
                                               energy_max=energy)

    #
    # extract the intensity
    #
    intensity, dim_x, dim_y = driver.calculate_intensity(srw_wavefront)


    # # Do some tests.
    # # assert abs(1.7063003e+09 - intensity[10, 10])<1e+6, \
    # #     'Quick verification of intensity value'
    # flux = intensity.sum() * (dim_x[1]-dim_x[0]) * (dim_y[1]-dim_y[0])
    # print("Total flux = %10.5e photons/s/.1%%bw"%flux)
    # if example_index == 0:
    #     assert abs(2.40966e+08 - flux)<1e+3, \
    #         'Quick verification of intensity value'
    # else:
    #     assert abs(2.14704e+07 - flux)<1e+3, \
    #         'Quick verification of intensity value'

    # Calculate phases.
    #phase = driver.calculate_phase(srw_wavefront)


    # # Do some tests.
    # checksum = np.sum( np.abs(srw_wavefront.arEx) ) + np.abs( np.sum(srw_wavefront.arEy) )
    # print("checksum is: ",checksum)
    #
    # if example_index == 0:
    #     assert np.abs(checksum - 1.1845644e+10) < 1e3, "Test electric field checksum"
    # else:
    #     assert np.abs(checksum - 1.53895e+13) < 1e8, "Test electric field checksum"

    return srw_wavefront, dim_x, dim_y, intensity

def test_bending_magnet_infrared_srw():
    srw_wavefront, dim_x, dim_y, intensity = run_bending_magnet_srw(0)

    flux = intensity.sum() * (dim_x[1]-dim_x[0]) * (dim_y[1]-dim_y[0])
    print("Total flux = %10.5e photons/s/.1%%bw"%flux)
    assert abs(2.40966e+08 - flux)<1e+3, \
        'Quick verification of intensity value'

    checksum = np.sum( np.abs(srw_wavefront.arEx) ) + np.abs( np.sum(srw_wavefront.arEy) )
    print("checksum is: ",checksum)
    assert np.abs(checksum - 1.1845644e+10) < 1e3, "Test electric field checksum"

    return srw_wavefront, dim_x, dim_y, intensity

def test_bending_magnet_xrays_srw():
    srw_wavefront, dim_x, dim_y, intensity = run_bending_magnet_srw(1)

    flux = intensity.sum() * (dim_x[1]-dim_x[0]) * (dim_y[1]-dim_y[0])
    print("Total flux = %10.5e photons/s/.1%%bw"%flux)
    assert abs(2.14704e+07 - flux)<1e+3, \
        'Quick verification of intensity value'

    checksum = np.sum( np.abs(srw_wavefront.arEx) ) + np.abs( np.sum(srw_wavefront.arEy) )
    print("checksum is: ",checksum)
    assert np.abs(checksum - 1.53895e+13) < 1e8, "Test electric field checksum"
    return srw_wavefront, dim_x, dim_y, intensity


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import time

    example_index = 0 # 0=infrared example,  1=x-ray ESRF example

    if example_index == 0:
        srw_wavefront, dim_x, dim_y, intensity = test_bending_magnet_infrared_srw()
        print('Calling plots with array shape: ',intensity.shape,'...')
        t0_main = time.time()
        plt.pcolormesh(dim_x,dim_y,intensity.transpose())
        plt.title("Real space for infrared example")
        plt.colorbar()
        print('done in', round(time.time() - t0_main), 's')
        plt.show()
    else:
        srw_wavefront, dim_x, dim_y, intensity = test_bending_magnet_xrays_srw()
        print('Calling plots with array shape: ',intensity.shape,'...')
        t0_main = time.time()
        plt.pcolormesh(dim_x,dim_y,intensity.transpose())
        plt.title("Real space for xrays example")
        plt.colorbar()
        print('done in', round(time.time() - t0_main), 's')
        plt.show()