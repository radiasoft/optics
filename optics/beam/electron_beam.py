"""
Base class for electron beams.
Every electron beam can carry settings, i.e. inherits DriverSettingManager.

This class is intentionally shorten for simplicity.
Usually we would need to consider also the electron distribution within the beam.
"""

from optics.driver.driver_setting_manager import DriverSettingManager

class ElectronBeam(DriverSettingManager):
    def __init__(self, energy_in_GeV, energy_spread, current, electrons_per_bunch,
                 moment_xx, moment_xxp, moment_xpxp,
                 moment_yy, moment_yyp, moment_ypyp):

        DriverSettingManager.__init__(self)

        self._energy_in_GeV = energy_in_GeV
        self._energy_spread = energy_spread
        self._current = current
        self._electrons_per_bunch = electrons_per_bunch

        self._moment_xx   = moment_xx
        self._moment_xxp  = moment_xxp
        self._moment_xpxp = moment_xpxp
        self._moment_yy   = moment_yy
        self._moment_yyp  = moment_yyp
        self._moment_ypyp = moment_ypyp

    # useful methods
    def gamma(self):
        #TODO: get the physical constant from a central repository
        return self._energy_in_GeV/0.51099890221e-03 # Relative Energy