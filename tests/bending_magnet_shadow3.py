"""
Example illustrating a possible implementation of "beamline components" / "a glossary".
May need python3 to run.
"""

import os

from examples.shadow.driver.shadow_driver import ShadowDriver

from optics.beam.electron_beam import ElectronBeam
from optics.source.bending_magnet import BendingMagnet

from optics.beamline.optical_elements.lens.lens_ideal import LensIdeal
from optics.beamline.optical_elements.image_plane import ImagePlane

from optics.beamline.beamline import Beamline
from optics.beamline.beamline_position import BeamlinePosition

from examples.shadow.sources.shadow_bending_magnet import ShadowBendingMagnetSetting

###################################################################################################
# Stage 1: abstract definition of the setting (electron beam, radiation source, beamline)
# We want to put everything in generic classes that is independent of a specific implementation.
# These are basically the information a scientist would need to physically build the beamline.
#
# Clearly we need extra information/settings to perform a calculation. And the extra settings
# vary for different programs. We provide these extra information by attaching program depended
# "settings".
###################################################################################################



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

        # Attach the component at its position to the beamline.
        self.attachComponentAt(lens, lens_position)

        # Attach a screen/image plane.
        plane_position = BeamlinePosition(10.0)
        self.attachComponentAt(ImagePlane("Image screen"), plane_position)


###################################################################################################
# Stage 3: calculate the radiation
###################################################################################################


def minimal_plot(shadow_beam):
    driver = ShadowDriver()
    int_grid, dim_x,dim_y = driver.calculateIntensity(shadow_beam)
    plt.pcolormesh(dim_x,dim_y,int_grid)
    plt.colorbar()

def test_conformance1():
    # Specify to use Shadow
    driver = ShadowDriver()

    electron_beam = ElectronBeam(energy_in_GeV=3.0,energy_spread=0.01,average_current=0.5,electrons_per_bunch=1)
    bending_magnet = BendingMagnet(radius=2.25,magnetic_field=0.4,length=2.25*0.100)

    # Attach SHADOW bending magnet settings.
    shadow_bending_magnet_settings = ShadowBendingMagnetSetting()
    shadow_bending_magnet_settings._e_max = 0.0600
    shadow_bending_magnet_settings._e_min = 0.0600
    shadow_bending_magnet_settings._number_of_rays = 26000
    shadow_bending_magnet_settings._calculation_mode = 1
    shadow_bending_magnet_settings._max_vertical_half_divergence_from = 0.01
    shadow_bending_magnet_settings._max_vertical_half_divergence_to = 0.01

    bending_magnet.addSettings(shadow_bending_magnet_settings)

    # Calculate the radiation.
    #TODO: rename radiation_source by magnetic_structure
    shadow_beam = driver.calculateRadiation(electron_beam=electron_beam,
                                          radiation_source=bending_magnet,
                                          beamline=ID1234())

    intensity,dim_x,dim_y = driver.calculateIntensity(shadow_beam)


    import matplotlib.pyplot as plt
    plt.pcolormesh(dim_x,dim_y,intensity.transpose())
    plt.colorbar()
    plt.show()

    os.remove("effic.01")
    os.remove("mirr.01")
    os.remove("rmir.01")
    os.remove("SPER00000")
    os.remove("optax.01")
    os.remove("star.01")
    os.remove("FLUX")
    os.remove("SPAR00000")
    os.remove("STOT00000")

if __name__ == "__main__":
    test_conformance1()