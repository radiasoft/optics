"""
Implements SRW Undulator settings.

It is completely up to driver developer to design this object.
The only requirement is that it inherits from AbstractDriverSetting that is initialized with the driver it belongs to.
"""
from optics.driver.abstract_driver_setting import AbstractDriverSetting


class SRWUndulatorSetting(AbstractDriverSetting):
    def __init__(self):
        from code_drivers.SRW.SRW_driver import SRWDriver
        AbstractDriverSetting.__init__(self,
                                       driver=SRWDriver())

        self._meth        = 1         #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
        self._relPrec     = 0.01      #relative precision
        self._zStartInteg = 0         #longitudinal position to start integration (effective if < zEndInteg)
        self._zEndInteg   = 0         #longitudinal position to finish integration (effective if > zStartInteg)
        self._npTraj      = 20000     #Number of points for trajectory calculation
        self._useTermin   = 1         #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
        self._sampFactNxNyForProp = 2 #sampling factor for adjusting nx, ny (effective if > 0)

    def toList(self):
        precision_parameter = [self._meth,
                               self._relPrec,
                               self._zStartInteg,
                               self._zEndInteg,
                               self._npTraj,
                               self._useTermin,
                               self._sampFactNxNyForProp]

        return precision_parameter
