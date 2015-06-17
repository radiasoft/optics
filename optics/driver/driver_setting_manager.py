"""
Manages driver settings.

Can store multiple settings for different drivers.
Every ElectronBeam,Source and BeamlineComponent is/has a DriverSettingsManager, i.e. can store driver depended settings.
"""

class DriverSettingManager(object):
    def __init__(self):
        """
        Constructor
        """
        self._driver_settings = []

    def add_settings(self, driver_settings):
        """
        Adds some settings
        :param driver_settings: Settings to set.
        """
        if self.has_settings(driver_settings.driver()):
            raise Exception("For the given driver, some settings have already been stored.")

        self._driver_settings.append(driver_settings)

    def remove_settings(self, driver):
        """
        Removes settings for a given driver.
        :param driver: The driver to remove settings for.
        """
        if not self.has_settings(driver):
            raise Exception("Can not remove settings for the given driver, because none have been stored.")

        driver_settings = self.settings(driver)
        self._driver_settings.remove(driver_settings)

    def set_settings(self, driver_settings):
        """
        Sets the given settings. Possible previously set settings for the same driver will be overwritten.
        :param driver_settings: Settings to set.
        """
        if self.has_settings(driver_settings.driver()):
            self.remove_settings(driver_settings.driver())
        self.add_settings(driver_settings)

    def settings(self, driver):
        """
        Returns the settings for a given driver.
        :param driver: driver to look for settings.
        :return: Returns the first settings stored for the given driver. Or None if there are no settings for the given driver.
        """
        for driver_settings in self._driver_settings:
            if driver_settings.is_driver(driver):
                return driver_settings

        return None

    def has_settings(self, driver):
        """
        Checks if there are settings for the given driver.
        :param driver: driver to check for attached settings.
        :return: True if there are settings for the given driver. False otherwise.
        """
        has_driver = self.settings(driver) is not None
        return has_driver