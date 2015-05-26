__author__ = 'labx'

import Shadow

class ShadowSource(object):
    def __init__(self):
        self._oe_number = 0

    def toNativeShadowSource(self):
        raise NotImplementedError()

    def fromNativeShadowSource(self, src):
        raise NotImplementedError()

    def fromNativeShadowSourceFile(self, file_name):
        src = Shadow.Source()
        src.load(file_name)

        self.fromNativeShadowSource(src)

    def newInstance(self):
        raise NotImplementedError

    def duplicate(self):
        src = self.toNativeShadowSource()
        new_src = Shadow.Source()

        new_src.OE_NUMBER =  0
        new_src.FILE_TRAJ=b"NONESPECIFIED"
        new_src.FILE_SOURCE=b"NONESPECIFIED"
        new_src.FILE_BOUND=b"NONESPECIFIED"

        new_src.FDISTR            = src.FDISTR
        new_src.FGRID             = src.FGRID
        new_src.FSOUR             = src.FSOUR
        new_src.FSOURCE_DEPTH     = src.FSOURCE_DEPTH
        new_src.F_COHER           = src.F_COHER
        new_src.F_COLOR           = src.F_COLOR
        new_src.F_PHOT            = src.F_PHOT
        new_src.F_POL             = src.F_POL
        new_src.F_POLAR           = src.F_POLAR
        new_src.F_OPD             = src.F_OPD
        new_src.F_WIGGLER         = src.F_WIGGLER
        new_src.F_BOUND_SOUR      = src.F_BOUND_SOUR
        new_src.F_SR_TYPE         = src.F_SR_TYPE
        new_src.ISTAR1            = src.ISTAR1
        new_src.NPOINT            = src.NPOINT
        new_src.NCOL              = src.NCOL
        new_src.N_CIRCLE          = src.N_CIRCLE
        new_src.N_COLOR           = src.N_COLOR
        new_src.N_CONE            = src.N_CONE
        new_src.IDO_VX            = src.IDO_VX
        new_src.IDO_VZ            = src.IDO_VZ
        new_src.IDO_X_S           = src.IDO_X_S
        new_src.IDO_Y_S           = src.IDO_Y_S
        new_src.IDO_Z_S           = src.IDO_Z_S
        new_src.IDO_XL            = src.IDO_XL
        new_src.IDO_XN            = src.IDO_XN
        new_src.IDO_ZL            = src.IDO_ZL
        new_src.IDO_ZN            = src.IDO_ZN
        new_src.SIGXL1            = src.SIGXL1
        new_src.SIGXL2            = src.SIGXL2
        new_src.SIGXL3            = src.SIGXL3
        new_src.SIGXL4            = src.SIGXL4
        new_src.SIGXL5            = src.SIGXL5
        new_src.SIGXL6            = src.SIGXL6
        new_src.SIGXL7            = src.SIGXL7
        new_src.SIGXL8            = src.SIGXL8
        new_src.SIGXL9            = src.SIGXL9
        new_src.SIGXL10           = src.SIGXL10
        new_src.SIGZL1            = src.SIGZL1
        new_src.SIGZL2            = src.SIGZL2
        new_src.SIGZL3            = src.SIGZL3
        new_src.SIGZL4            = src.SIGZL4
        new_src.SIGZL5            = src.SIGZL5
        new_src.SIGZL6            = src.SIGZL6
        new_src.SIGZL7            = src.SIGZL7
        new_src.SIGZL8            = src.SIGZL8
        new_src.SIGZL9            = src.SIGZL9
        new_src.SIGZL10           = src.SIGZL10
        new_src.CONV_FACT         = src.CONV_FACT
        new_src.CONE_MAX          = src.CONE_MAX
        new_src.CONE_MIN          = src.CONE_MIN
        new_src.EPSI_DX           = src.EPSI_DX
        new_src.EPSI_DZ           = src.EPSI_DZ
        new_src.EPSI_X            = src.EPSI_X
        new_src.EPSI_Z            = src.EPSI_Z
        new_src.HDIV1             = src.HDIV1
        new_src.HDIV2             = src.HDIV2
        new_src.PH1               = src.PH1
        new_src.PH2               = src.PH2
        new_src.PH3               = src.PH3
        new_src.PH4               = src.PH4
        new_src.PH5               = src.PH5
        new_src.PH6               = src.PH6
        new_src.PH7               = src.PH7
        new_src.PH8               = src.PH8
        new_src.PH9               = src.PH9
        new_src.PH10              = src.PH10
        new_src.RL1               = src.RL1
        new_src.RL2               = src.RL2
        new_src.RL3               = src.RL3
        new_src.RL4               = src.RL4
        new_src.RL5               = src.RL5
        new_src.RL6               = src.RL6
        new_src.RL7               = src.RL7
        new_src.RL8               = src.RL8
        new_src.RL9               = src.RL9
        new_src.RL10              = src.RL10
        new_src.BENER             = src.BENER
        new_src.POL_ANGLE         = src.POL_ANGLE
        new_src.POL_DEG           = src.POL_DEG
        new_src.R_ALADDIN         = src.R_ALADDIN
        new_src.R_MAGNET          = src.R_MAGNET
        new_src.SIGDIX            = src.SIGDIX
        new_src.SIGDIZ            = src.SIGDIZ
        new_src.SIGMAX            = src.SIGMAX
        new_src.SIGMAY            = src.SIGMAY
        new_src.SIGMAZ            = src.SIGMAZ
        new_src.VDIV1             = src.VDIV1
        new_src.VDIV2             = src.VDIV2
        new_src.WXSOU             = src.WXSOU
        new_src.WYSOU             = src.WYSOU
        new_src.WZSOU             = src.WZSOU
        new_src.PLASMA_ANGLE      = src.PLASMA_ANGLE
        new_src.FILE_TRAJ         = src.FILE_TRAJ
        new_src.FILE_SOURCE       = src.FILE_SOURCE
        new_src.FILE_BOUND        = src.FILE_BOUND
        new_src.OE_NUMBER         = src.OE_NUMBER
        new_src.NTOTALPOINT       = src.NTOTALPOINT
        new_src.IDUMMY            = src.IDUMMY
        new_src.DUMMY             = src.DUMMY
        new_src.F_NEW             = src.F_NEW

        new_shadow_source = self.newInstance()
        new_shadow_source.fromNativeShadowSource(new_src)

        return new_shadow_source