from optics.driver.abstract_driver_setting import AbstractDriverSetting


class ShadowDriverSetting(AbstractDriverSetting):

    def __init__(self):
        from code_drivers.shadow.driver.shadow_driver import ShadowDriver
        AbstractDriverSetting.__init__(self,
                                       driver=ShadowDriver())
