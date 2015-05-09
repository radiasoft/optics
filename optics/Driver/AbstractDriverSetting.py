"""
Abstract base class for driver settings.
"""

class AbstractDriverSetting(object):
    def __init__(self, driver):
        self._driver = driver

    def driver(self):
        return self._driver

    def isDriver(self, driver):

        try:
            is_driver = isinstance(self._driver, type(driver))
        except:
            is_driver = False

        return is_driver