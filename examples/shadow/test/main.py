__author__ = 'labx'

import sys
from PyQt4.QtGui import QApplication

from optics.beam.electron_beam import ElectronBeam
from optics.source.bending_magnet import BendingMagnet

from examples.shadow.driver.shadow_driver import ShadowDriver

def run_shadow():

   # Create the "glossary" object.
   electron_beam = ElectronBeam(6.04,1.0,0.200,1)
   bending_magnet = BendingMagnet(25.1772, 2.0)

   # Instantiate the driver.
   driver = ShadowDriver()

   # Calculate the beam without beamline.
   shadow_beam = driver.calculateRadiation(electron_beam=electron_beam,
                                           radiation_source=bending_magnet,
                                           beamline=None)

   # Return the "radiation object" which is a shadow beam in the shadow case.
   return shadow_beam

if __name__ == "__main__":
   a = QApplication(sys.argv)

   shadow_beam = run_shadow()

   # NOTE: Needs orange shadow to run.
   from orangecontrib.shadow.util.shadow_util import ShadowPlot
   plot = ShadowPlot.DetailedPlotWidget()
   plot.plotxy(shadow_beam._beam, 1, 3, "pippo", "X", "Z")

   plot.show()

   a.exec_()

