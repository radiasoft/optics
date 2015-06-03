__author__ = 'labx'
"""
Implements a bending magnet.
"""

from optics.source.source import Source

class BendingMagnet(Source):
    def __init__(self, radius, magnetic_field, energy):
        """
        Constructor.
        :param radius: Radius/curvature of the magnet.
        :param magnetic_field: Magnetic field strength.
        :param energy: Photon energy in eV.
        """
        Source.__init__(self)
        self._radius = radius
        self._magnetic_field = magnetic_field
        self.setEnergy(energy)

    def radius(self):
        return self._radius

    def magneticField(self):
        return self._magnetic_field