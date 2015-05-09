"""
Example illustrating a possible implementation of "beamline components" / "a glossary".
May need python3 to run.
"""
import pytest

from optics.Beam.ElectronBeam import ElectronBeam
from optics.Source.UndulatorVertical import UndulatorVertical
from optics.Lens.LensIdeal import LensIdeal
from optics.Beamline.Beamline import Beamline
from optics.Beamline.BeamlinePosition import BeamlinePosition

from optics.Driver.SRW.SRWDriver import SRWDriver
from optics.Driver.SRW.SRWBeamlineComponentSetting import SRWBeamlineComponentSetting

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
                              energy_in_GeV=6.04,
                              energy_spread=0.06,
                              average_current=0.2,
                              electrons=10**9)


# Define the radiation source - here an undulator (totally generic in this example)
class Undulator35(UndulatorVertical):
    def __init__(self):
        UndulatorVertical.__init__(self,
                                   K=1.87,
                                   period_length=0.035,
                                   periods_number=56)

# Define a beamline (generic + SRW specific settings)
class ID1234(Beamline):
    def __init__(self):
        Beamline.__init__(self)

        # Create a beamline that only has one lens attached.
        # First create the lens.
        lens=LensIdeal("focus lens",
                       focal_x=1.0,
                       focal_y=1.0)
        # Specify the position of the lens (could set extra parameters for: off-axis and inclination)
        lens_position = BeamlinePosition(1.0)

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
    # In case of shadow use SHADOWDriver().
    # This would be the only line to change - if sufficiently configured for shadow as well.
    driver = SRWDriver()

    # Calculate the radiation.
    radiation = driver.calculateRadiation(electron_beam=ESRFStorageRing(),
                                          radiation_source=Undulator35(),
                                          beamline=ID1234())

    # Calculate intensity.
    intensity = driver.calculateIntensity(radiation)
    # Calculate phases.
    phase = driver.calculatePhase(radiation)
    assert 1237847826759680.0 == intensity[0][9215], \
        'Quick verification of intensity value'

    #print(intensity)
    #print(phase)
