__author__ = 'labx'

import sys
import numpy as np
import matplotlib.pyplot as plt

from optics.beam.electron_beam import ElectronBeam
from optics.source.bending_magnet import BendingMagnet

from examples.shadow.driver.shadow_driver import ShadowDriver

def run_shadow():

   # Create the "glossary" object.
   electron_beam = ElectronBeam(6.04,1.0,0.200,1)
   bending_magnet = BendingMagnet(25.1772, 2.0,8000)

   # Instantiate the driver.
   driver = ShadowDriver()

   # Calculate the beam without beamline.
   shadow_beam = driver.calculateRadiation(electron_beam=electron_beam,
                                           radiation_source=bending_magnet,
                                           beamline=None)

   # Return the "radiation object" which is a shadow beam in the shadow case.
   return shadow_beam

def minimal_plot(shadow_beam):
    driver = ShadowDriver()
    int_grid, dim_x,dim_y = driver.calculateIntensity(shadow_beam)
    plt.pcolormesh(dim_x,dim_y,int_grid)
    plt.colorbar()
#    plt.show()

if __name__ == "__main__":
   shadow_beam = run_shadow()

   minimal_plot(shadow_beam)

   import Shadow.ShadowTools
   Shadow.ShadowTools.plotxy(shadow_beam._beam,1,2,contour=0)
 
   plt.show()

