#
# Python script to run srw bending magnet
#

from __future__ import print_function #Python 2.7 compatibility
from srwlib import *
from uti_plot import * #required for plotting
import time
import pytest

def bending_magnet_srw_raw_run():
    ###########################################################################
    # SRWLIB Example#13: Simulating propagation of bending magnet SR through a simple optical scheme
    # v 0.01
    #############################################################################



    print('SRWLIB Python Example # 13:')
    print('!!!!!Under testing!!!!!')
    print('Simulating emission and propagation of Bending Magnet Synchrotron Radiaiton wavefront through a simple beamline')

    #***********Data Folder and File Names
    strExDataFolderName = 'data_example_13' #example data sub-folder name
    strIntOutFileName0 = 'ex13_res_int0.dat' #file names for output SR intensity data
    strIntOutFileName1 = 'ex13_res_int_prop_se.dat'
    strIntOutFileName2 = 'ex13_res_int_prop_me.dat'

    #***********Bending Magnet
    B = 0.4 #Dipole magnetic field [T]
    LeffBM = 4. #Magnet length [T] (exaggerated, to skip eventual "edge radiation")
    BM = SRWLMagFldM(B, 1, 'n', LeffBM)
    magFldCnt = SRWLMagFldC([BM], array('d',[0]), array('d',[0]), array('d',[0])) #Container of magnetic field elements and their positions in 3D

    #***********Electron Beam
    eBeam = SRWLPartBeam()
    eBeam.Iavg = 0.5 #Average current [A]
    #1st order statistical moments:
    eBeam.partStatMom1.x = 0. #Initial horizontal position of central trajectory [m]
    eBeam.partStatMom1.y = 0. #Initial vertical position of central trajectory [m]
    eBeam.partStatMom1.z = 0. #Initial longitudinal position of central trajectory [m]
    eBeam.partStatMom1.xp = 0. #Initial horizontal angle of central trajectory [rad]
    eBeam.partStatMom1.yp = 0. #Initial vertical angle of central trajectory [rad]
    eBeam.partStatMom1.gamma = 3./0.51099890221e-03 #Relative energy
    #2nd order statistical moments:
    eBeam.arStatMom2[0] = (127.346e-06)**2 #<(x-x0)^2> [m^2]
    eBeam.arStatMom2[1] = -10.85e-09 #<(x-x0)*(x'-x'0)> [m]
    eBeam.arStatMom2[2] = (92.3093e-06)**2 #<(x'-x'0)^2>
    eBeam.arStatMom2[3] = (13.4164e-06)**2 #<(y-y0)^2>
    eBeam.arStatMom2[4] = 0.0072e-09 #<(y-y0)*(y'-y'0)> [m]
    eBeam.arStatMom2[5] = (0.8022e-06)**2 #<(y'-y'0)^2>
    eBeam.arStatMom2[10] = (0.89e-03)**2 #<(E-E0)^2>/E0^2

    #***********Radiation Sampling for the Initial Wavefront (before first optical element)
    wfr = SRWLWfr() #Wavefront structure (placeholder for data to be calculated)
    wfr.allocate(1, 10, 10) #Numbers of points vs photon energy, horizontal and vertical positions (the last two will be modified in the process of calculation)

    distSrcLens = 5. #Distance from geometrical source point to lens [m]
    wfr.mesh.zStart = distSrcLens #Longitudinal position for initial wavefront [m]

    wfr.mesh.eStart = 0.5*0.123984 #Initial photon energy [eV]
    #Calculations in this script were tested for photon energies between ~0.0124 and ~0.124 eV (~100 and ~10 microns respectively)
    wfr.mesh.eFin = wfr.mesh.eStart #Final photon energy [eV]

    horAng = 0.1 #Horizontal angle [rad]
    wfr.mesh.xStart = -0.5*horAng*distSrcLens #Initial horizontal position [m]
    wfr.mesh.xFin = 0.5*horAng*distSrcLens #Final horizontal position [m]
    verAng = 0.02 #Vertical angle [rad]
    wfr.mesh.yStart = -0.5*verAng*distSrcLens #Initial vertical position [m]
    wfr.mesh.yFin = 0.5*verAng*distSrcLens #Final vertical position [m]
    wfr.partBeam = eBeam #e-beam data is contained inside wavefront struct

    #***********Optical Elements and their Corresponding Propagation Parameters
    distLensImg = distSrcLens #Distance from lens to image plane
    focLen = wfr.mesh.zStart*distLensImg/(distSrcLens + distLensImg)
    optLens = SRWLOptL(_Fx=focLen, _Fy=focLen) #Thin lens
    optDrift = SRWLOptD(distLensImg) #Drift space from lens to image plane

    #Propagation paramaters (SRW specific)
    #                [0][1][2] [3][4] [5] [6] [7] [8]
    propagParLens =  [1, 1, 1., 0, 0, 1., 2., 1., 2., 0, 0, 0]
    propagParDrift = [1, 1, 1., 0, 0, 1., 1., 1., 1., 0, 0, 0]
    #Wavefront Propagation Parameters:
    #[0]: Auto-Resize (1) or not (0) Before propagation
    #[1]: Auto-Resize (1) or not (0) After propagation
    #[2]: Relative Precision for propagation with Auto-Resizing (1. is nominal)
    #[3]: Allow (1) or not (0) for semi-analytical treatment of the quadratic (leading) phase terms at the propagation
    #[4]: Do any Resizing on Fourier side, using FFT, (1) or not (0)
    #[5]: Horizontal Range modification factor at Resizing (1. means no modification)
    #[6]: Horizontal Resolution modification factor at Resizing
    #[7]: Vertical Range modification factor at Resizing
    #[8]: Vertical Resolution modification factor at Resizing
    #[9]: Type of wavefront Shift before Resizing (not yet implemented)
    #[10]: New Horizontal wavefront Center position after Shift (not yet implemented)
    #[11]: New Vertical wavefront Center position after Shift (not yet implemented)

    #"Beamline" - Container of optical elements (together with their corresponding wavefront propagation parameters / instructions)
    optBL = SRWLOptC([optLens, optDrift], [propagParLens, propagParDrift])

    #***********BM SR Calculation
    #Precision parameters
    meth = 2 #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
    relPrec = 0.01 #Relative precision
    zStartInteg = 0 #Longitudinal position to start integration (effective if < zEndInteg)
    zEndInteg = 0 #Longitudinal position to finish integration (effective if > zStartInteg)
    npTraj = 20000 #Number of points for trajectory calculation
    useTermin = 1 #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
    sampFactNxNyForProp = 0.7 #Sampling factor for adjusting nx, ny (effective if > 0)
    arPrecSR = [meth, relPrec, zStartInteg, zEndInteg, npTraj, useTermin, sampFactNxNyForProp]

    print('   Performing initial electric field calculation ... ', end='')
    t0 = time.time()
    srwl.CalcElecFieldSR(wfr, 0, magFldCnt, arPrecSR)
    print('done in', round(time.time() - t0), 's')

    print('   Extracting intensity from calculated electric field and saving it to file(s) ... ', end='')
    t0 = time.time()
    mesh0 = deepcopy(wfr.mesh)
    arI0 = array('f', [0]*mesh0.nx*mesh0.ny) #"Flat" array to take 2D intensity data (vs X & Y)
    srwl.CalcIntFromElecField(arI0, wfr, 6, 0, 3, mesh0.eStart, 0, 0)
#    srwl_uti_save_intens_ascii(arI0, mesh0, os.path.join(os.getcwd(), strExDataFolderName, strIntOutFileName0), 0)
    print('done in', round(time.time() - t0), 's')

    #***********Wavefront Propagation
    print('   Simulating single-electron electric field wavefront propagation ... ', end='')
    t0 = time.time()
    srwl.PropagElecField(wfr, optBL)
    print('done in', round(time.time() - t0), 's')

    print('   Extracting intensity from calculated electric field and saving it to file(s) ... ', end='')
    t0 = time.time()


    return wfr

#     mesh1 = deepcopy(wfr.mesh)
#     arI1s = array('f', [0]*mesh1.nx*mesh1.ny) #"Flat" array to take 2D single-electron intensity data (vs X & Y)
#     srwl.CalcIntFromElecField(arI1s, wfr, 6, 0, 3, mesh1.eStart, 0, 0) #Extracting single-electron intensity vs X & Y
#     srwl_uti_save_intens_ascii(arI1s, mesh1, os.path.join(os.getcwd(), strExDataFolderName, strIntOutFileName1), 0)
#
#     arI1m = deepcopy(arI1s) #"Flat" array to take 2D multi-electron intensity data (vs X & Y)
#     srwl.CalcIntFromElecField(arI1m, wfr, 6, 1, 3, mesh1.eStart, 0, 0) #Calculating multi-electron intensity vs X & Y using convolution method (assuming it to be valid!)
#     srwl_uti_save_intens_ascii(arI1m, mesh1, os.path.join(os.getcwd(), strExDataFolderName, strIntOutFileName2), 0)
#
#     print('done in', round(time.time() - t0), 's')
#
#     #***********Plotting the Calculation Results
#     unitsInPlot = ['m', 'm', 'ph/s/.1%bw/mm^2']
#     uti_plot2d1d(arI0, [mesh0.xStart, mesh0.xFin, mesh0.nx], [mesh0.yStart, mesh0.yFin, mesh0.ny], labels=('Horizontal position', 'Vertical position', 'Intensity before Lens'), units=unitsInPlot)
#     uti_plot2d1d(arI1s, [mesh1.xStart, mesh1.xFin, mesh1.nx], [mesh1.yStart, mesh1.yFin, mesh1.ny], labels=('Horizontal position', 'Vertical position', 'Single-E Intensity in Image Plane'), units=unitsInPlot)
#     uti_plot2d1d(arI1m, [mesh1.xStart, mesh1.xFin, mesh1.nx], [mesh1.yStart, mesh1.yFin, mesh1.ny], labels=('Horizontal position', 'Vertical position', 'Multi-E Intensity in Image Plane'), units=unitsInPlot)
#
#     uti_plot_show() #show all graphs (blocks script execution; close all graph windows to proceed)


def test_srw_raw():
    #calculate the wavefront for a single electron
    wfr = bending_magnet_srw_raw_run()
    #plot image plane
    mesh1 = deepcopy(wfr.mesh)
    arI1s = array('f', [0]*mesh1.nx*mesh1.ny) #"Flat" array to take 2D single-electron intensity data (vs X & Y)
    srwl.CalcIntFromElecField(arI1s, wfr, 6, 0, 3, mesh1.eStart, 0, 0) #Extracting single-electron intensity vs X & Y
    unitsInPlot = ['m', 'm', 'ph/s/.1%bw/mm^2']
    uti_plot2d1d(arI1s, [mesh1.xStart, mesh1.xFin, mesh1.nx], [mesh1.yStart, mesh1.yFin, mesh1.ny], labels=('Horizontal position', 'Vertical position', 'Single-E Intensity in Image Plane'), units=unitsInPlot)
    uti_plot_show() #show all graphs (blocks script execution; close all graph windows to proceed)


