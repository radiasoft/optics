"""
Base class for electron beams.
Every electron beam can carry settings, i.e. inherits DriverSettingManager.

This class is intentionally shorten for simplicity.
Usually we would need to consider also the electron distribution within the beam.
"""

from optics.Driver.DriverSettingManager import DriverSettingManager


class ElectronBeam(DriverSettingManager):
    def __init__(self, energy_in_GeV, energy_spread, average_current, electrons):

        DriverSettingManager.__init__(self)

        self._energy = energy_in_GeV
        self._energy_spread = energy_spread
        self._average_current = average_current
        self.setElectrons(electrons)

    def energy(self):
        return self._energy

    def gamma(self):
        return self.energy()/0.51099890221e-03 # Relative Energy

    def averageCurrent(self):
        return self._average_current

    def setElectrons(self, electrons):
        self._electrons = electrons

    def electrons(self):
        return self._electrons

    def x(self):
        # TODO: for simplity. Add distribution in long run.
        return 0.0

    def y(self):
        # TODO: for simplity. Add distribution in long run.
        return 0.0