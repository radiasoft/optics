#
# Python script to run srw bending magnet
#

from __future__ import print_function #Python 2.7 compatibility
from srwlib import *
from tests.utilities.uti_plot import * #required for plotting
import time
import pytest

def run_bending_magnet_srw(example_index):
    # set example_index=0 for infrared example and example_index=1 for xrays example

    if example_index == 0:
         ###########################################################################
         # SRWLIB Example#13 (option for BM infrared BL): Simulating propagation of bending magnet SR through a simple optical scheme
         # v 0.01
         #############################################################################
         print('SRWLIB Python Example # 13 (option for BM infrared BL):')
         print('!!!!!Under testing!!!!!')
         print('Simulating emission and propagation of Bending Magnet Synchrotron Radiaiton wavefront through a simple beamline')


    else:
        ###########################################################################
        # SRWLIB Example#13 (option for BM X-ray BL): Simulating propagation of bending magnet SR through a simple optical scheme
        # v 0.01
        #############################################################################
        print('SRWLIB Python Example # 13 (option for BM X-ray BL):')
        print('!!!!!Under testing!!!!!')
        print('Simulating emission and propagation of Bending Magnet Synchrotron Radiaiton wavefront through a simple beamline')

    print('   Setting parameters ... ',end="\n")

    t0_setting = time.time()

    #***********Bending Magnet
    if example_index == 0:
         B = 0.4 #Dipole magnetic field [T]
         LeffBM = 4. #Magnet length [T] (exaggerated, to skip eventual "edge radiation")
    else:
        B = 0.86 #0.4 #Dipole magnetic field [T]
        LeffBM = 0.5 #4. #Magnet length [m] (exaggerated, to skip eventual "edge radiation")

    BM = SRWLMagFldM(B, 1, 'n', LeffBM)
    magFldCnt = SRWLMagFldC([BM], array('d',[0]), array('d',[0]), array('d',[0])) #Container of magnetic field elements and their positions in 3D

    #***********Electron Beam
    eBeam = SRWLPartBeam()

    if example_index  == 0:
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
    else:
        eBeam.Iavg = 0.2 #Average current [A]
        #1st order statistical moments:
        eBeam.partStatMom1.x = 0. #Initial horizontal position of central trajectory [m]
        eBeam.partStatMom1.y = 0. #Initial vertical position of central trajectory [m]
        eBeam.partStatMom1.z = 0. #Initial longitudinal position of central trajectory [m]
        eBeam.partStatMom1.xp = 0. #Initial horizontal angle of central trajectory [rad]
        eBeam.partStatMom1.yp = 0. #Initial vertical angle of central trajectory [rad]
        eBeam.partStatMom1.gamma = 6./0.51099890221e-03 #Relative energy
        #2nd order statistical moments:
        eBeam.arStatMom2[0] = (77.9e-06)**2 #(127.346e-06)**2 #<(x-x0)^2> [m^2]
        eBeam.arStatMom2[1] = 0. #-10.85e-09 #<(x-x0)*(x'-x'0)> [m]
        eBeam.arStatMom2[2] = (110.9e-06)**2 #(92.3093e-06)**2 #<(x'-x'0)^2>
        eBeam.arStatMom2[3] = (12.9e-06)**2 #(13.4164e-06)**2 #<(y-y0)^2>
        eBeam.arStatMom2[4] = 0 #0.0072e-09 #<(y-y0)*(y'-y'0)> [m]
        eBeam.arStatMom2[5] = (0.5e-06)**2 #(0.8022e-06)**2 #<(y'-y'0)^2>
        eBeam.arStatMom2[10] = (0.89e-03)**2 #<(E-E0)^2>/E0^2


    #***********Radiation Sampling for the Initial Wavefront (before first optical element)
    wfr = SRWLWfr() #Wavefront structure (placeholder for data to be calculated)
    wfr.allocate(1, 10, 10) #Numbers of points vs photon energy, horizontal and vertical positions (the last two will be modified in the process of calculation)
    if example_index == 0:
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
    else:
        distSrcLens = 25. #Distance from geometrical source point to lens [m]
        wfr.mesh.zStart = distSrcLens #Longitudinal position for initial wavefront [m]

        wfr.mesh.eStart = 15000 #Initial photon energy [eV]
        wfr.mesh.eFin = wfr.mesh.eStart #Final photon energy [eV]

        #The script was tested / tuned for the two cases of the horizontal acceptance angle: 4 mrad and 1 mrad
        #horAng = 4.e-03 #Horizontal acceptance angle [rad]
        horAng = 1.e-03 #Horizontal acceptance angle [rad]

        wfr.mesh.xStart = -0.5*horAng*distSrcLens #Initial horizontal position [m]
        wfr.mesh.xFin = 0.5*horAng*distSrcLens #Final horizontal position [m]
        verAng = 0.4e-03 #Vertical angle [rad]
        wfr.mesh.yStart = -0.5*verAng*distSrcLens #Initial vertical position [m]
        wfr.mesh.yFin = 0.5*verAng*distSrcLens #Final vertical position [m]
        wfr.partBeam = eBeam #e-beam data is contained inside wavefront struct

    #***********Optical Elements and their Corresponding Propagation Parameters
    if example_index == 0:
         distLensImg = distSrcLens #Distance from lens to image plane
         focLen = wfr.mesh.zStart*distLensImg/(distSrcLens + distLensImg)
         optLens = SRWLOptL(_Fx=focLen, _Fy=focLen) #Thin lens
         optDrift = SRWLOptD(distLensImg) #Drift space from lens to image plane

         #Propagation paramaters (SRW specific)
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
    else:
        distLensImg = distSrcLens #Distance from lens to image plane
        focLen = distSrcLens*distLensImg/(distSrcLens + distLensImg)
        optLens = SRWLOptL(_Fx=focLen, _Fy=focLen) #Thin lens
        optDrift = SRWLOptD(distLensImg) #Drift space from lens to image plane

        #Propagation paramaters (SRW specific)
        #X-ray BM SR case: propagation without "auto-resizing"
        #and with semi-analytical treatment of the quadratic phase terms, to save memory
        propagParLens =  [0, 0, 1., 0, 0, 1., 5., 1., 3., 0, 0, 0]
        propagParDrift = [0, 0, 1., 1, 0, 1., 1., 1., 1., 0, 0, 0]
        #Increasing ranges after propagation for multi-e estimation by convolution
        #and eventuall resampling down the resulting wavefront to save memory:
        propagParFin =   [0, 0, 1., 0, 0, 1.2,0.3,1.5,1., 0, 0, 0]

        if(horAng <= 1.e-03): #Tuning propagation parameters for different BL parameters (horizontal angular aperture)
            propagParLens =  [0, 0, 1., 0, 0, 1., 5., 1., 8., 0, 0, 0]
            propagParFin =   [0, 0, 1., 0, 0, 4., 1.,1.5, 1., 0, 0, 0]

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
        #optBL = SRWLOptC([optLens, optDrift], [propagParLens, propagParDrift])

        optBL = SRWLOptC([optLens, optDrift], [propagParLens, propagParDrift, propagParFin])


    print('   done in', round(time.time() - t0_setting), 's')


    #***********BM SR Calculation
    #Precision parameters
    meth = 2 #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
    relPrec = 0.01 #Relative precision
    if example_index == 0:

         zStartInteg = 0 #Longitudinal position to start integration (effective if < zEndInteg)
         zEndInteg = 0 #Longitudinal position to finish integration (effective if > zStartInteg)
         npTraj = 20000 #Number of points for trajectory calculation
         useTermin = 1 #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
         sampFactNxNyForProp = 0.7 #Sampling factor for adjusting nx, ny (effective if > 0)
         arPrecSR = [meth, relPrec, zStartInteg, zEndInteg, npTraj, useTermin, sampFactNxNyForProp]

         print('   Performing initial electric field calculation ... ', end='\n')
         t0 = time.time()
         srwl.CalcElecFieldSR(wfr, 0, magFldCnt, arPrecSR)
         print('   done in', round(time.time() - t0), 's')

         print('   Extracting intensity from calculated electric field and saving it to file(s) ... ', end='\n')
         t0 = time.time()
         mesh0 = deepcopy(wfr.mesh)
         arI0 = array('f', [0]*mesh0.nx*mesh0.ny) #"Flat" array to take 2D intensity data (vs X & Y)
         srwl.CalcIntFromElecField(arI0, wfr, 6, 0, 3, mesh0.eStart, 0, 0)
         print('   done in', round(time.time() - t0), 's')
    else:
        if(horAng <= 1.e-03): relPrec = 0.003
        zStartInteg = 0 #Longitudinal position to start integration (effective if < zEndInteg)
        zEndInteg = 0 #Longitudinal position to finish integration (effective if > zStartInteg)
        npTraj = 20000 #Number of points for trajectory calculation
        useTermin = 1 #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
        sampFactNxNyForProp = 0.0035 #Sampling factor for adjusting nx, ny for propagation (effective if > 0)
        arPrecSR = [meth, relPrec, zStartInteg, zEndInteg, npTraj, useTermin, sampFactNxNyForProp]

        print('   Performing initial electric field calculation ... ', end='\n')
        t0 = time.time()
        srwl.CalcElecFieldSR(wfr, 0, magFldCnt, arPrecSR)
        print('   done in', round(time.time() - t0), 's')

        print('   Extracting intensity from calculated electric field and saving it to file(s) ... ', end='\n')
        t0 = time.time()
        mesh0 = deepcopy(wfr.mesh)
        arI0 = array('f', [0]*mesh0.nx*mesh0.ny) #"Flat" array to take 2D intensity data (vs X & Y)
        srwl.CalcIntFromElecField(arI0, wfr, 6, 0, 3, mesh0.eStart, 0, 0)
        print('   done in', round(time.time() - t0), 's')

    if example_index == 0:
         #***********Wavefront Propagation
         print('   Simulating single-electron electric field wavefront propagation ... ', end='\n')
         t0 = time.time()
         srwl.PropagElecField(wfr, optBL)
         print('   done in', round(time.time() - t0), 's')

    else:
        #***********Wavefront Propagation
        print('   Simulating single-electron electric field wavefront propagation ... ', end='\n')
        t0 = time.time()
        srwl.PropagElecField(wfr, optBL)
        print('   done in', round(time.time() - t0), 's')


    return wfr

def test_bending_magnet_infrared_srw_native():
    wfr = run_bending_magnet_srw(0)
    checksum = np.sum( np.abs(wfr.arEx) ) + np.abs( np.sum(wfr.arEy) )
    print("   Checksum is :  %f\n"%checksum)
    assert np.abs(checksum - 11845644288)  < 1e3, "Test electric field checksum"
    return wfr


def test_bending_magnet_xrays_srw_native():
    wfr = run_bending_magnet_srw(1)
    checksum = np.sum( np.abs(wfr.arEx) ) + np.abs( np.sum(wfr.arEy) )
    print("   Checksum is :  %f\n"%checksum)
    assert np.abs(checksum - 15389542055936)  < 1e3, "Test electric field checksum"
    return wfr



if __name__ == "__main__":

    example_index = 0  # 0=infrared example,  1=x-ray ESRF example

    print('Calling test_bending_magnet_srw_native ... ', end='\n')
    t0_main = time.time()


    if example_index == 0:
        wfr = test_bending_magnet_infrared_srw_native()
    else:
        wfr = test_bending_magnet_xrays_srw_native()

    print('done in', round(time.time() - t0_main), 's')

    print('Calling plots ... ', end='\n')
    t0_main = time.time()

    #plot image plane
    mesh1 = deepcopy(wfr.mesh)
    arI1s = array('f', [0]*mesh1.nx*mesh1.ny) #"Flat" array to take 2D single-electron intensity data (vs X & Y)
    srwl.CalcIntFromElecField(arI1s, wfr, 6, 1, 3, mesh1.eStart, 0, 0) #Extracting single-electron intensity vs X & Y

    unitsInPlot = ['m', 'm', 'ph/s/.1%bw/mm^2']
    uti_plot2d1d(arI1s, [mesh1.xStart, mesh1.xFin, mesh1.nx], [mesh1.yStart, mesh1.yFin, mesh1.ny], labels=('Horizontal position', 'Vertical position', 'Single-E Intensity in Image Plane'), units=unitsInPlot)
    uti_plot_show() #show all graphs (blocks script execution; close all graph windows to proceed)
    print('done in', round(time.time() - t0_main), 's')
