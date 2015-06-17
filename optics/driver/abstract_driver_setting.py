"""
Abstract base class for driver settings.
"""

class AbstractDriverSetting(object):
    def __init__(self, driver):
        self._driver = driver

    def driver(self):
        return self._driver

    def is_driver(self, driver):

        try:
            is_driver = type(self._driver) is type(driver)
        except:
            is_driver = False

        return is_driver