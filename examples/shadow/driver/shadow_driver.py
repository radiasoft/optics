__author__ = 'labx'

from optics.driver.abstract_driver import AbstractDriver
from optics.source.bending_magnet import BendingMagnet

from examples.shadow.driver.shadow_beam import ShadowBeam
from examples.shadow.sources.shadow_bending_magnet import ShadowBendingMagnet, ShadowBendingMagnetSetting


class ShadowDriver(AbstractDriver):

    def processSource(self, source):
        return self.traceFromSource(source)

    def processComponent(self, beamline_component, previous_result):
        return self.traceFromOE(beamline_component, previous_result)

    def calculateRadiation(self,electron_beam, radiation_source, beamline):
        """
        Calculates radiation.

        :param electron_beam: ElectronBeam object
        :param radiation_source: Source object
        :param beamline: Beamline object
        :return: ShadowBeam.
        """

        if isinstance(radiation_source, BendingMagnet):

            # If BendingMagnet is not configured for shadow add default settings.
            if not radiation_source.hasSettings(ShadowDriver()):
                radiation_source.addSettings(ShadowBendingMagnetSetting())

            # Create a ShadowSource for shadow API.
            shadow_source = ShadowBendingMagnet(electron_beam, radiation_source)
        else:
            raise NotImplementedError


        # Calculate the source's radiation / shadow beam with the shadow API.
        shadow_beam = self.processSource(shadow_source)

        return shadow_beam
    #-----------------------------------------------------

    def traceFromSource(self, shadow_source):
        return ShadowBeam.traceFromSource(shadow_source)

    def traceFromOE(self, shadow_oe, input_shadow_beam):
        return ShadowBeam.traceFromOE(shadow_oe, input_shadow_beam)
