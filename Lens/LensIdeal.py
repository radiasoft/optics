"""
Represents an ideal lens.
"""
from BeamlineComponent import BeamlineComponent


class LensIdeal(BeamlineComponent):
    def __init__(self, name, focal_x, focal_y):
        BeamlineComponent.__init__(self, name=name)
        self._focal_x = focal_x
        self._focal_y = focal_y

    def focalX(self): 
        return self._focal_x

    def focalY(self):
        return self._focal_y