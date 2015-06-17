"""
Base class for all radiation sources: bending magnet or insertion devices (wiggler, undulator)
Every source can attach settings, i.e. inherits from DriverSettingsManager.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from optics.driver.driver_setting_manager import DriverSettingManager


class MagneticStructure(DriverSettingManager):
    def __init__(self):
        DriverSettingManager.__init__(self)

        self.setEnergy(8000)

    def setEnergy(self, energy):
        """
        Sets source radiation energy. For the moment only a single energy line.
        :param energy: Source energy line in eV.
        """
        self._energy = energy

    def energy(self):
        """
        Returns source radiation energy. For the moment only a single energy line.
        :return: Source energy line in eV.
        """
        return self._energy
