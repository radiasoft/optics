__author__ = 'labx'
"""
Implements a bending magnet.
"""

from optics.source.source import Source

class BendingMagnet(Source):
    def __init__(self, radius, magnetic_field, length):
        """
        Constructor.
        :param radius: Physical Radius/curvature of the magnet in m
        :param magnetic_field: Magnetic field strength in T
        :param length: physical length of the bending magnet (along the arc) in m.
        """
        Source.__init__(self)
        self._radius = radius
        self._magnetic_field = magnetic_field
        self._length = length
        #TODO remove
        #self.setEnergy(energy)

    #TODO remove these setters and getters? If removed, prefer to name variables without underscore.
    def radius(self):
        return self._radius

    def magnetic_field(self):
        return self._magnetic_field

    def set_length(self,length):
        self._length = length

    def set_radius(self, radius):
        self._radius = radius

    def set_magnetic_field(self,magnetic_field):
        self._magnetic_field = magnetic_field

    def length(self):
        return self._length

    #
    #methods for practical calculations
    #
    def horizontal_divergence(self):
        return self.length()/self.radius()

    def to_dictionary(self):
        return {'__name__':'bending_magnet','_radius':self.radius(), '_magnetic_field':self.magnetic_field(), '_length':self.length()}