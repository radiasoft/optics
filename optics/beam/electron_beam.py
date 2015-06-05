"""
Base class for electron beams.
Every electron beam can carry settings, i.e. inherits DriverSettingManager.

This class is intentionally shorten for simplicity.
Usually we would need to consider also the electron distribution within the beam.
"""

from optics.driver.driver_setting_manager import DriverSettingManager


class ElectronBeam(DriverSettingManager):
    def __init__(self, energy_in_GeV, energy_spread, average_current, electrons_per_bunch):

        DriverSettingManager.__init__(self)

        self._energy_in_GeV = energy_in_GeV
        self._energy_spread = energy_spread
        self._average_current = average_current
        self._electrons_per_bunch = electrons_per_bunch


    #TODO: remove setters and getters?

    def set_electrons_per_bunch(self, electrons_per_bunch):
        self._electrons_per_bunch = electrons_per_bunch

    def electrons_per_bunch(self):
        return self._electrons_per_bunch

    def energy_in_GeV(self):
        return self._energy_in_GeV

    def average_current(self):
        return self._average_current



    # useful methods

    def gamma(self):
        return self._energy_in_GeV/0.51099890221e-03 # Relative Energy

    def x(self):
        # TODO: for simplity. Add distribution in long run.
        return 0.0

    def y(self):
        # TODO: for simplity. Add distribution in long run.
        return 0.0

    def to_dictionary(self):
        return {'__name__':'electron_beam','_energy_in_GeV':self._energy_in_GeV, '_energy_spread':self._energy_spread,
                '_average_current':self._average_current, '_electrons_per_bunch':self._electrons_per_bunch}