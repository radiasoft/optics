__author__ = 'labx'

import sys
import numpy as np
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

def gaussianBroadedIntensity(rays):
    rays_y = rays[:,0]
    rays_x = rays[:,1]
    I = np.sum(np.array([ rays[:,i]*rays[:,i] for i in [6,7,8] ]),axis=0)

    n_x = 250
    n_y = 250
    dim_x = np.linspace(rays_x.min(),rays_x.max(),n_x)
    dim_y = np.linspace(rays_y.min(),rays_y.max(),n_y)
    int_grid = np.zeros((n_x,n_y))

    sigma = min(dim_x[1]-dim_x[0],
                dim_y[1]-dim_y[0])/2.0
    four_sigma = 4*sigma

    for pos_x,pos_y,pos_int in zip(rays_x,rays_y,I):
        for i_x in range(dim_x.shape[0]):

            if np.abs(pos_x - dim_x[i_x]) > four_sigma:
                continue

            int_grid[i_x,:] += np.exp(-((pos_x - dim_x[i_x])**2 + (pos_y-dim_y)**2)/sigma)


    return dim_x,dim_y, int_grid

def plot(rays):
    import matplotlib.pyplot as plt
    import pylab
    import Shadow.ShadowToolsPrivate as stp
    x = rays[:,0]
    y = rays[:,1]
    z = np.sum(np.array([ rays[:,i]*rays[:,i] for i in [6,7,8] ]),axis=0)

    col1 = x
    col2 = y
    col4 = z

    t = np.where(col1!=-3299)
    xrange = stp.setGoodRange(col1[t])
    yrange = stp.setGoodRange(col2[t])

    tx = np.where((col1>xrange[0])&(col1<xrange[1]))
    ty = np.where((col2>yrange[0])&(col2<yrange[1]))

    tf = set(list(t[0])) & set(list(tx[0])) & set(list(ty[0]))
    t = (np.array(sorted(list(tf))),)

    figure = pylab.plt.figure(figsize=(12,8),dpi=96)

    ratio = 8.0/12.0
    left, width = 0.1*ratio, 0.65*ratio
    bottom, height = 0.1, 0.65
    bottom_h = bottom+height+0.02
    left_h = left+width+0.02*ratio

    #rect_scatter = [0.10*ratio, 0.10, 0.65*ratio, 0.65]
    #rect_histx =   [0.10*ratio, 0.77, 0.65*ratio, 0.20]
    #rect_histy =   [0.77*ratio, 0.10, 0.20*ratio, 0.65]
    #rect_text =    [1.00*ratio, 0.10, 1.20*ratio, 0.65]


    #axScatter = figure.add_axes(rect_scatter)
    #axScatter.set_xlabel(xtitle)
    #axScatter.set_ylabel(ytitle)

    #axScatter.scatter(col1[t],col2[t],s=0.5)
    #pylab.plt.show()
    #figure.show()

    dim_x,dim_y, int_grid = gaussianBroadedIntensity(rays)
    plt.pcolormesh(dim_x,dim_y,int_grid)
    plt.show()

if __name__ == "__main__":
   a = QApplication(sys.argv)

   shadow_beam = run_shadow()

   import Shadow.ShadowTools
   Shadow.ShadowTools.plotxy(shadow_beam._beam,1,2,contour=0)
   plot(shadow_beam._beam.rays)

   # NOTE: Needs orange shadow to run.
   from orangecontrib.shadow.util.shadow_util import ShadowPlot
   plot = ShadowPlot.DetailedPlotWidget()
   plot.plotxy(shadow_beam._beam, 1, 3, "pippo", "X", "Z")

   plot.show()

   a.exec_()

