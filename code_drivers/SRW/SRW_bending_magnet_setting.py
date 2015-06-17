"""
Implements SRW bending magnet settings.

It is completely up to driver developer to design this object.
The only requirement is that it inherits from AbstractDriverSetting that is initialized with the driver it belongs to.
"""
from code_drivers.SRW.SRW_driver_setting import SRWDriverSetting


class SRWBendingMagnetSetting(SRWDriverSetting):
    def __init__(self):
        SRWDriverSetting.__init__(self)

        self._meth        = 2           #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
        self._relPrec     = 0.01        #relative precision
        self._zStartInteg = 0           #longitudinal position to start integration (effective if < zEndInteg)
        self._zEndInteg   = 0           #longitudinal position to finish integration (effective if > zStartInteg)
        self._npTraj      = 20000       #Number of points for trajectory calculation
        self._useTermin   = 1           #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
        self._sampFactNxNyForProp = 0.7 #sampling factor for adjusting nx, ny (effective if > 0)

        # TODO: check meaningfulness of these default values
        self._horizontal_acceptance_angle = 0.1
        self._vertical_acceptance_angle   = 0.01

    def to_list(self):
        precision_parameter = [self._meth,
                               self._relPrec,
                               self._zStartInteg,
                               self._zEndInteg,
                               self._npTraj,
                               self._useTermin,
                               self._sampFactNxNyForProp]

        return precision_parameter

    def set_acceptance_angle(self, horizontal_angle, vertical_angle):
        self._horizontal_acceptance_angle = horizontal_angle
        self._vertical_acceptance_angle   = vertical_angle

    def horizontal_acceptance_angle(self):
        return self._horizontal_acceptance_angle

    def vertical_acceptance_angle(self):
        return self._vertical_acceptance_angle