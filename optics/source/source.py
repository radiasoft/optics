"""
Base class for all radiation sources: bending magnet or insertion devices (wiggler, undulator)
Every source can attach settings, i.e. inherits from DriverSettingsManager.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from optics.driver.driver_setting_manager import DriverSettingManager


class Source(DriverSettingManager):
    def __init__(self):
        DriverSettingManager.__init__(self)
