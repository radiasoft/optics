__author__ = 'labx'

import sys
from PyQt4.QtGui import QApplication

from examples.shadow.driver.shadow_driver import ShadowDriver
from examples.shadow.sources.shadow_bending_magnet import ShadowBendingMagnet

def run_shadow():
   driver = ShadowDriver()

   bending_magnet = ShadowBendingMagnet()

   shadow_beam = driver.processSource(bending_magnet)

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

