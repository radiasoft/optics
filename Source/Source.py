"""
Base class for all radiation sources: bending magnet or insertion devices (wiggler, undulator)
Every source can attach settings, i.e. inherits from DriverSettingsManager.
"""

from Driver.DriverSettingManager import DriverSettingManager


class Source(DriverSettingManager):
    def __init__(self):
        DriverSettingManager.__init__(self)