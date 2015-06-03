"""
Example illustrating a possible implementation of "beamline components" / "a glossary".
May need python3 to run.
"""
from examples.SRW.SRW_driver import SRWDriver
from examples.SRW.SRW_bending_magnet_setting import SRWBendingMagnetSetting
from examples.SRW.SRW_beamline_component_setting import SRWBeamlineComponentSetting

from optics.beam.electron_beam import ElectronBeam
from optics.source.bending_magnet import BendingMagnet

from optics.beamline.optical_elements.lens.lens_ideal import LensIdeal
from optics.beamline.optical_elements.image_plane import ImagePlane

from optics.beamline.beamline import Beamline
from optics.beamline.beamline_position import BeamlinePosition

###################################################################################################
# Stage 1: abstract definition of the setting (electron beam, radiation source, beamline)
# We want to put everything in generic classes that is independent of a specific implementation.
# These are basically the information a scientist would need to physically build the beamline.
#
# Clearly we need extra information/settings to perform a calculation. And the extra settings
# vary for different programs. We provide these extra information by attaching program depended
# "settings".
###################################################################################################


# Define the electron beam of the machine (totally generic in this example)
class ESRFStorageRing(ElectronBeam):
    def __init__(self):
        ElectronBeam.__init__(self,
                              energy_in_GeV=3.0,
                              energy_spread=0.01,
                              average_current=0.5,
                              electrons=10**9)


# Define a beamline (generic + SRW specific settings)
class ID1234(Beamline):
    def __init__(self):
        Beamline.__init__(self)

        # Create a beamline that only has one lens attached.
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


        # We could also _simultaneously_ add settings for shadow here:
        # lens_setting = ShadowBeamlineComponentSetting()
        # lens_setting.setSOMETHING(..)
        # lens.addSettings(lens_setting)
        # The lens would be configured _simultaneously_ for SRW and SHADOW.

        # Attach the component at its position to the beamline.
        self.attachComponentAt(lens, lens_position)

        # Attach a screen/image plane.
        plane_position = BeamlinePosition(10.0)
        self.attachComponentAt(ImagePlane("Image screen"), plane_position)

###################################################################################################
# Stage 2: attach settings to a generic beamline in case it was not done in stage 1 already.
###################################################################################################
# We could also add shadow and/or srw settings later.
#beamline = ID1234()
#focus_lens = beamline.componentByName("focus lens")
#lens_setting = SRWBeamlineComponentSetting()
#lens_setting.setResizeResolutionHorizontal(5.0)
#focus_lens.setSettings(lens_setting)

# Personally I like more to set up everything in one place, i.e. to set up everything in stage 1.
# However, one could take a SRW configured beamline and add quickly the necessary
# shadow settings without change the original script.



###################################################################################################
# Stage 3: calculate the radiation
###################################################################################################

def test_conformance1():
    # Specify to use SRW.
    driver = SRWDriver()

    # Define the bending magnet source.
    effecitve_bending_magnet_length = 4. #Magnet length [T] (exaggerated, to skip eventual "edge radiation")
    # TODO: do the right conversion.
    radius = 1.0/effecitve_bending_magnet_length
    bending_magnet = BendingMagnet(radius=radius,
                                   magnetic_field=0.4,
                                   energy=0.5*0.123984)

    # Attach SRW bending magnet settings.
    # NOTE: Maybe angular acceptance is generic and should move to BendingMagnet or Source class??
    srw_bending_magnet_setting = SRWBendingMagnetSetting()
    srw_bending_magnet_setting.setAcceptanceAngle(horizontal_angle=0.1,
                                                  vertical_angle=0.02)
    bending_magnet.addSettings(srw_bending_magnet_setting)

    # Calculate the radiation.
    radiation = driver.calculateRadiation(electron_beam=ESRFStorageRing(),
                                          radiation_source=bending_magnet,
                                          beamline=ID1234())

    # Calculate intensity.
    intensity, dim_x,dim_y = driver.calculateIntensity(radiation)
    # Calculate phases.
    phase = driver.calculatePhase(radiation)
    assert abs(1.7063003e+09 - intensity[10, 10])<1e+6, \
        'Quick verification of intensity value'

    import matplotlib.pyplot as plt
    print(dim_x.shape)
    print(dim_y.shape)
    print(intensity.shape)
    plt.pcolormesh(dim_x,dim_y,intensity.transpose())
    plt.colorbar()
    plt.show()