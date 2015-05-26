"""
Driver template.
Every program (SRW, SHADOW, ...) must implement a driver with the following methods.
"""

class AbstractDriver(object):
    def calculateRadiation(self,electron_beam, radiation_source, beamline):
        """
        Calculates radiation.

        :param electron_beam: ElectronBeam object
        :param radiation_source: Source object
        :param beamline: beamline object
        :return: Radiation object. The driver is free to design this object as it likes it. The only requirement is that
        this object is used to calculate intensity, phase, ... That means the driver needs to understands this object.
        In the case of SRW this would be something carrying the wavefront in shadow it would be a beam.
        """
        raise Exception("Needs reimplementation")

    def calculateIntensity(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Intensity in some generic form/object to be defined.
        """
        raise Exception("Needs reimplementation")

    def calculatePhase(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Phases in some generic form/object to be defined.
        """
        raise Exception("Needs reimplementation")