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

    #
    #methods for practical calculations
    #
    def horizontal_divergence(self):
        return self.length()/self.radius()