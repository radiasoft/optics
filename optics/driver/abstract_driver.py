"""
Driver template.
Every program (SRW, SHADOW, ...) must implement a driver with the following methods.
"""

class AbstractDriver(object):
    def calculate_radiation(self,electron_beam, radiation_source, beamline, energy_min, energy_max):
        """
        Calculates radiation.

        :param electron_beam: ElectronBeam object
        :param radiation_source: Source object
        :param beamline: beamline object
        :param energy_min: Minimal energy for the calculation
        :param energy_max: Maximal energy for the calculation
        :return: Radiation object. The driver is free to design this object as it likes it. The only requirement is that
        this object is used to calculate intensity, phase, ... That means the driver needs to understands this object.
        In the case of SRW this would be something carrying the wavefront in shadow it would be a beam.
        """
        raise Exception("Needs reimplementation")

    def calculate_intensity(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Intensity in some generic form/object to be defined.
        """
        raise Exception("Needs reimplementation")

    def calculate_phase(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Phases in some generic form/object to be defined.
        """
        raise Exception("Needs reimplementation")