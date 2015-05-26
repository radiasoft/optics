__author__ = 'labx'
"""
Implements a bending magnet.
"""

from optics.source.source import Source

class BendingMagnet(Source):
    def __init__(self, radius, magnetic_field):
        """
        Constructor.
        :param radius: Radius/curvature of the magnet.
        :param magnetic_field: Magnetic field strength.
        """
        Source.__init__(self)
        self._radius = radius
        self._magnetic_field = magnetic_field

    def radius(self):
        return self._radius

    def magneticField(self):
        return self._magnetic_field