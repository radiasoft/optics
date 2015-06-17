"""
Example of a bending magnet emitting in infrared region for a single electron emission
"""

# Import elements from common Glossary
from optics.beam.electron_beam_pencil import ElectronBeamPencil
from optics.magnetic_structures.bending_magnet import BendingMagnet

from optics.beamline.optical_elements.lens.lens_ideal import LensIdeal
from optics.beamline.optical_elements.image_plane import ImagePlane

from optics.beamline.beamline import Beamline
from optics.beamline.beamline_position import BeamlinePosition

#import Shadow driver and particular settings of the glossary elements used
from code_drivers.SRW.SRW_driver import SRWDriver
from code_drivers.SRW.SRW_bending_magnet_setting import SRWBendingMagnetSetting
from code_drivers.SRW.SRW_beamline_component_setting import SRWBeamlineComponentSetting


###################################################################################################
# Stage 1: abstract definition of the setting (electron beam, radiation source, beamline)
# We want to put everything in generic classes that is independent of a specific implementation.
# These are basically the information a scientist would need to physically build the beamline.
#
# Clearly we need extra information/settings to perform a calculation. And the extra settings
# vary for different programs. We provide these extra information by attaching program depended
# "settings".
###################################################################################################
#
#
# # Define a beamline (generic + SRW specific settings)
# class ID1234(Beamline):
#     def __init__(self):
#         Beamline.__init__(self)
#
#         # Create a beamline that only has one lens attached.
#         # First create the lens.
#         lens=LensIdeal("focus lens",
#                        focal_x=2.5,
#                        focal_y=2.5)
#         # Specify the position of the lens (could set extra parameters for: off-axis and inclination)
#         lens_position = BeamlinePosition(5.0)
#
#         # Set settings for SRW.
#         # These are settings that depend on the "driver" to use.
#         # If no special settings are set the driver will use its default settings.
#         # If we do not wand to increase the resolution we can go with standard settings and would just remove the following 4 lines.
#         lens_setting = SRWBeamlineComponentSetting()
#         lens_setting.setResizeResolutionHorizontal(2.0)
#         lens_setting.setResizeResolutionVertical(2.0)
#         lens.addSettings(lens_setting)
#
#
#         # We could also _simultaneously_ add settings for shadow here:
#         # lens_setting = ShadowBeamlineComponentSetting()
#         # lens_setting.setSOMETHING(..)
#         # lens.addSettings(lens_setting)
#         # The lens would be configured _simultaneously_ for SRW and SHADOW.
#
#         # Attach the component at its position to the beamline.
#         self.attachComponentAt(lens, lens_position)
#
#         # Attach a screen/image plane.
#         plane_position = BeamlinePosition(10.0)
#         self.attachComponentAt(ImagePlane("Image screen"), plane_position)
#
#
# ###################################################################################################
# # Stage 3: calculate the radiation
# ###################################################################################################

def test_bending_magnet_srw():
    # Specify to use SRW.
    driver = SRWDriver()

    #
    # 1) define first the electron beam
    #
    electron_beam = ElectronBeamPencil(energy_in_GeV=3.0,energy_spread=0.01,current=0.5)

    #
    # 2) define the magnetic structure
    #
    bending_magnet = BendingMagnet(radius=2.25,magnetic_field=0.4,length=4.0)


    # Attach SRW bending magnet settings.
    #TODO: angular acceptance is used to define screen size.
    # NOTE: Maybe angular acceptance is generic and should move to BendingMagnet or Source class??
    srw_bending_magnet_setting = SRWBendingMagnetSetting()
    srw_bending_magnet_setting.set_acceptance_angle(horizontal_angle=0.1,
                                                    vertical_angle=0.02)
    energy = 0.5*0.123984
    srw_bending_magnet_setting.set_energy_min(energy)
    srw_bending_magnet_setting.set_energy_max(energy)
    bending_magnet.addSettings(srw_bending_magnet_setting)

    #
    # 3) define beamline containing the optical elements
    #    In this case, create a beamline that only has one lens attached plus an image (detector) plane
    #

    #
    beamline  = Beamline()

    # First create the lens.
    lens=LensIdeal("focus lens",
                   focal_x=2.5,
                   focal_y=2.5)
    # Specify the position of the lens (could set extra parameters for: off-axis and inclination)
    lens_position = BeamlinePosition(5.0)

    # Set settings for SRW.
    # These are settings that depend on the "driver" to use.
    # If no special settings are set the driver will use its default settings.
    # If we do not wand to increase the resolution we can go with standard settings and would just remove the following 4 lines.
    lens_setting = SRWBeamlineComponentSetting()
    lens_setting.setResizeResolutionHorizontal(2.0)
    lens_setting.setResizeResolutionVertical(2.0)
    lens.addSettings(lens_setting)


    # Attach the component at its position to the beamline.
    beamline.attachComponentAt(lens, lens_position)

    # Attach a screen/image plane.
    plane_position = BeamlinePosition(10.0)
    beamline.attachComponentAt(ImagePlane("Image screen"), plane_position)




    #
    #  Calculate the radiation (i.e., run the codes). It returns a native SRWLWfr()
    #
    srw_wavefront = driver.calculateRadiation(electron_beam=electron_beam,
                                              magnetic_structure=bending_magnet,
                                              beamline=beamline)

    #
    # extract and plot the intensity
    #
    intensity, dim_x,dim_y = driver.calculateIntensity(srw_wavefront)
    # Calculate phases.
    phase = driver.calculatePhase(srw_wavefront)
    assert abs(1.7063003e+09 - intensity[10, 10])<1e+6, \
        'Quick verification of intensity value'

    import matplotlib.pyplot as plt
    plt.pcolormesh(dim_x,dim_y,intensity.transpose())
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    test_bending_magnet_srw()