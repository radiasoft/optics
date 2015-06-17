"""
Implements SRW ElectronBeam settings.

It is completely up to driver developer to design this object.
The only requirement is that it inherits from AbstractDriverSetting that is initialized with the driver it belongs to.

Although we use only one ElectronBeam Setting object in this example it is easily possible to use multiple if needed/wished.
"""
from code_drivers.SRW.SRW_driver_setting import SRWDriverSetting

class ElectronBeamSetting(SRWDriverSetting):
    def __init__(self):
        SRWDriverSetting.__init__(self)


