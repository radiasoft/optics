__author__ = 'labx'


import Shadow
import numpy

from code_drivers.shadow.driver.shadow_driver_setting import ShadowDriverSetting
from code_drivers.shadow.sources.shadow_source import ShadowSource

class ShadowBendingMagnet(ShadowSource):
    def __init__(self, electron_beam, bending_magnet, energy_min, energy_max):
        ShadowSource.__init__(self)
        self._electron_beam = electron_beam
        self._bending_magnet = bending_magnet
        self._energy_min = energy_min
        self._energy_max = energy_max

    def newInstance(self):
        return ShadowBendingMagnet(self._electron_beam,
                                   self._bending_magnet,
                                   self._energy_min,
                                   self._energy_max)

    def toNativeShadowSource(self):
        src = Shadow.Source()

        src.FSOURCE_DEPTH=4
        src.F_COLOR=3
        src.F_PHOT=0
        src.F_POLAR=1
        src.NCOL=0
        src.N_COLOR=0
        src.POL_DEG=0.0

        #TODO: not needed?
        src.SIGDIX=0.0
        src.SIGDIZ=0.0
        src.SIGMAY=0.0
        src.WXSOU=0.0
        src.WYSOU=0.0
        src.WZSOU=0.0
        src.F_WIGGLER = 0
        src.F_OPD = 1
        src.F_SR_TYPE = 0


        from code_drivers.shadow.driver.shadow_driver import ShadowDriver
        settings = self._bending_magnet.settings(ShadowDriver())

        # NOTE: photon energy is set on bending magnet.
        # Energy is sync to settings object to avoid possible side effects - if any possible.
        # settings._e_min = self._bending_magnet.energy()
        # settings._e_max = self._bending_magnet.energy()

        src.NPOINT = settings._number_of_rays
        src.ISTAR1 = settings._seed

        # Set energy range.
        src.PH1 = self._energy_min
        src.PH2 = self._energy_max

        src.F_POL = 1 + settings._generate_polarization

        #this come from electron beam
        src.SIGMAX = 100.0*numpy.sqrt(self._electron_beam._moment_xx) #  settings._sigma_x
        src.SIGMAZ = 100.0*numpy.sqrt(self._electron_beam._moment_yy) # settings._sigma_z
        src.EPSI_X = 100.0*numpy.sqrt(self._electron_beam._moment_xx)*numpy.sqrt(self._electron_beam._moment_xpxp)
        src.EPSI_Z = 100.0*numpy.sqrt(self._electron_beam._moment_yy)*numpy.sqrt(self._electron_beam._moment_ypyp)
        src.EPSI_DX = settings._distance_from_waist_x
        src.EPSI_DZ = settings._distance_from_waist_z

        # Energy is stored in ElectronBeam
        src.BENER = self._electron_beam._energy_in_GeV

        src.R_ALADDIN = -100*self._bending_magnet._radius # -2501.0459 # physical radius in cm
        src.R_MAGNET = self._bending_magnet._radius  # 3.334728*self._electron_beam._energy_in_GeV/self._bending_magnet._magnetic_field # magnetic radius in m

        src.HDIV1 = 0.5*self._bending_magnet._length/self._bending_magnet._radius # 0.0500000007
        src.HDIV2 = 0.5*self._bending_magnet._length/self._bending_magnet._radius  # 0.0500000007
        src.VDIV1 = settings._max_vertical_half_divergence_from
        src.VDIV2 = settings._max_vertical_half_divergence_to
        src.FDISTR = 4 + 2 * settings._calculation_mode
        src.F_BOUND_SOUR = settings._optimize_source
        src.FILE_BOUND = bytes(settings._optimize_file_name, 'utf-8')
        src.NTOTALPOINT = settings._max_number_of_rejected_rays

        if 1:
            src.write("start.00-1")
            print("File written to disk start.00-1")
        return src

    #TODO remove this method? What's the interest? Do not set glossary objects from here...
    def fromNativeShadowSource(self, src):
        from code_drivers.shadow.driver.shadow_driver import ShadowDriver
        settings = self._bending_magnet.settings(ShadowDriver())

        settings._number_of_rays=src.NPOINT
        settings._seed=src.ISTAR1
        self._energy_min=src.PH1
        self._energy_max=src.PH2
        settings._store_optical_paths=src.F_OPD
        settings._sample_distribution=src.F_SR_TYPE
        settings._generate_polarization=src.F_POL-1

        #TODO: belongs to ElectronBeam
        settings._sigma_x=src.SIGMAX
        settings._sigma_z=src.SIGMAZ
        settings._emittance_x=src.EPSI_X
        settings._emittance_z=src.EPSI_Z

        # TODO: belongs to ElectronBeam
        settings._energy=src.BENER
        settings._distance_from_waist_x=src.EPSI_DX
        settings._distance_from_waist_z=src.EPSI_DZ

        # TODO: belongs to BendingMagnet
        #settings._magnetic_radius=src.R_MAGNET

        settings._horizontal_half_divergence_from=src.HDIV1
        settings._horizontal_half_divergence_to=src.HDIV2
        settings._max_vertical_half_divergence_from=src.VDIV1
        settings._max_vertical_half_divergence_to=src.VDIV2
        settings._calculation_mode = (src.FDISTR-4)/2

        settings._optimize_source = src.F_BOUND_SOUR
        settings._optimize_file_name = src.FILE_BOUND.decode("utf-8")

        if not src.NTOTALPOINT is None:
            settings._max_number_of_rejected_rays = src.NTOTALPOINT
        else:
            settings._max_number_of_rejected_rays = 10000000


class ShadowBendingMagnetSetting(ShadowDriverSetting):
    def __init__(self):
        ShadowDriverSetting.__init__(self)

        self._number_of_rays = 50000
        self._seed = 6775431
        self._generate_polarization = 2

        #TODO:  belongs to ElectronBeam
        self._sigma_x = 0.0 #0.0078
        self._sigma_z = 0.0 #0.0036
        self._emittance_x = 0.0 #3.8E-7
        self._emittance_z = 0.0 #3.8E-9
        self._distance_from_waist_x = 0.0
        self._distance_from_waist_z = 0.0

        self._horizontal_half_divergence_from = 0.0005
        self._horizontal_half_divergence_to = 0.0005
        self._max_vertical_half_divergence_from = 1.0
        self._max_vertical_half_divergence_to = 1.0
        self._calculation_mode = 0
        self._optimize_source = 0
        self._optimize_file_name = "NONE SPECIFIED"
        self._max_number_of_rejected_rays = 10000000

