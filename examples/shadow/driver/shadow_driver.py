__author__ = 'labx'

from optics.driver.abstract_driver import AbstractDriver

from examples.shadow.driver.shadow_beam import ShadowBeam

class ShadowDriver(AbstractDriver):

    def processSource(self, source):
       return self.traceFromSource(source)

    def processComponent(self, beamline_component, previous_result):
        return self.traceFromOE(beamline_component, previous_result)

    #-----------------------------------------------------

    def traceFromSource(self, shadow_source):
        return ShadowBeam.traceFromSource(shadow_source)

    def traceFromOE(self, shadow_oe, input_shadow_beam):
        return ShadowBeam.traceFromOE(shadow_oe, input_shadow_beam)
