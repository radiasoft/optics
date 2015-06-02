__author__ = 'labx'


import Shadow

from optics.driver.abstract_driver_setting import AbstractDriverSetting
from examples.shadow.sources.shadow_source import ShadowSource

class ShadowBendingMagnet(ShadowSource):
    def __init__(self, electron_beam, bending_magnet):
        ShadowSource.__init__(self)
        self._electron_beam = electron_beam
        self._bending_magnet = bending_magnet

    def newInstance(self):
        return ShadowBendingMagnet(self._electron_beam,
                                   self._bending_magnet)

    def toNativeShadowSource(self):
        src = Shadow.Source()

        src.FSOURCE_DEPTH=4
        src.F_COLOR=3
        src.F_PHOT=0
        src.F_POLAR=1
        src.NCOL=0
        src.N_COLOR=0
        src.POL_DEG=0.0
        src.SIGDIX=0.0
        src.SIGDIZ=0.0
        src.SIGMAY=0.0
        src.WXSOU=0.0
        src.WYSOU=0.0
        src.WZSOU=0.0
        src.F_WIGGLER = 0
        src.F_OPD = 1
        src.F_SR_TYPE = 0

        from examples.shadow.driver.shadow_driver import ShadowDriver
        settings = self._bending_magnet.settings(ShadowDriver())

        src.NPOINT = settings._number_of_rays
        src.ISTAR1 = settings._seed
        src.PH1 = settings._e_min
        src.PH2 = settings._e_max
        src.F_POL = 1 + settings._generate_polarization
        src.SIGMAX = settings._sigma_x
        src.SIGMAZ = settings._sigma_z
        src.EPSI_X = settings._emittance_x
        src.EPSI_Z = settings._emittance_z

        # Energy is stored in ElectronBeam
        src.BENER = self._electron_beam._energy

        src.EPSI_DX = settings._distance_from_waist_x
        src.EPSI_DZ = settings._distance_from_waist_z

        # Radius is stored in BendingMagnet
        src.R_MAGNET  = self._bending_magnet.radius()
        src.R_ALADDIN = self._bending_magnet.radius() * 100

        src.HDIV1 = settings._horizontal_half_divergence_from
        src.HDIV2 = settings._horizontal_half_divergence_to
        src.VDIV1 = settings._max_vertical_half_divergence_from
        src.VDIV2 = settings._max_vertical_half_divergence_to
        src.FDISTR = 4 + 2 * settings._calculation_mode
        src.F_BOUND_SOUR = settings._optimize_source
        src.FILE_BOUND = bytes(settings._optimize_file_name, 'utf-8')
        src.NTOTALPOINT = settings._max_number_of_rejected_rays

        return src

    def fromNativeShadowSource(self, src):
        from examples.shadow.driver.shadow_driver import ShadowDriver
        settings = self._bending_magnet.settings(ShadowDriver())

        settings._number_of_rays=src.NPOINT
        settings._seed=src.ISTAR1
        settings._e_min=src.PH1
        settings._e_max=src.PH2
        settings._store_optical_paths=src.F_OPD
        settings._sample_distribution=src.F_SR_TYPE
        settings._generate_polarization=src.F_POL-1

        settings._sigma_x=src.SIGMAX
        settings._sigma_z=src.SIGMAZ
        settings._emittance_x=src.EPSI_X
        settings._emittance_z=src.EPSI_Z

        # TODO: belongs to ElectronBeam
        #settings._energy=src.BENER
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


class ShadowBendingMagnetSetting(AbstractDriverSetting):
    def __init__(self):
        from examples.shadow.driver.shadow_driver import ShadowDriver
        AbstractDriverSetting.__init__(self,
                                       driver=ShadowDriver())

        self._number_of_rays = 50000
        self._seed = 6775431
        self._e_min = 5000
        self._e_max = 100000
        self._generate_polarization = 2
        self._sigma_x = 0.0078
        self._sigma_z = 0.0036
        self._emittance_x = 3.8E-7
        self._emittance_z = 3.8E-9
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

