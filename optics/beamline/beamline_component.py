"""
Base class for all beamline components.
Enforce to name every every component.
Every beamline component can store settings (inherits from DriverSettingsManager)
"""

from optics.driver.driver_setting_manager import DriverSettingManager


class BeamlineComponent(DriverSettingManager):
    def __init__(self, name):
        self._name = name
        DriverSettingManager.__init__(self)

    def name(self):
        return self._name