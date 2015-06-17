from optics.driver.abstract_driver_setting import AbstractDriverSetting

class SRWDriverSetting(AbstractDriverSetting):
    def __init__(self):
        from code_drivers.SRW.SRW_driver import SRWDriver
        AbstractDriverSetting.__init__(self,
                                       driver=SRWDriver())
