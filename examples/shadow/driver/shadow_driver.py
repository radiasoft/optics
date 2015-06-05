__author__ = 'labx'
import numpy as np
import Shadow

from optics.driver.abstract_driver import AbstractDriver
from optics.source.bending_magnet import BendingMagnet

from optics.beamline.beamline_position import BeamlinePosition

from optics.beamline.optical_elements.lens.lens_ideal import LensIdeal
from optics.beamline.optical_elements.image_plane import ImagePlane

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
            raise NotImplementedError("Only Bending Magnet implemented right now")


        # Calculate the source's radiation / shadow beam with the shadow API.
        shadow_beam = self.processSource(shadow_source)

        i = 0
        for component in beamline:
            i += 1
            position = beamline.positionOf(component)

            previous_component = beamline.previousComponent(component)
            if previous_component is None:
                position_previous_component = BeamlinePosition(0.0)
            else:
                position_previous_component = beamline.positionOf(next_component)


            next_component = beamline.nextComponent(component)
            if next_component is None:
                break
            position_next_component = beamline.positionOf(next_component)

            shadow_oe = Shadow.OE()

            if isinstance(component, LensIdeal):

                q = position_next_component.z() - position.z()
                q *= 100.0 # to cm

                p = position.z() - position_previous_component.z()
                p *= 100.0 # to cm

                shadow_oe.FMIRR = 2
                shadow_oe.HOLO_W = 4879.85986
                shadow_oe.NCOL = 0
                shadow_oe.R_LAMBDA = 5000.0
                shadow_oe.T_IMAGE = q
                shadow_oe.T_INCIDENCE = 20.0
                shadow_oe.T_REFLECTION = 20.0
                shadow_oe.T_SOURCE = p

                shadow_oe.F_DEFAULT = 0
                shadow_oe.SIMAG = 2*component.focalY()*100.0
                shadow_oe.SSOUR = 2*component.focalY()*100.0
                shadow_oe.THETA = 20.0
            elif isinstance(component, ImagePlane):
                continue
            else:
                raise NotImplementedError

            shadow_beam._beam.traceOE(shadow_oe,i)


        return shadow_beam
    #-----------------------------------------------------

    def traceFromSource(self, shadow_source):
        return ShadowBeam.traceFromSource(shadow_source)

    def traceFromOE(self, shadow_oe, input_shadow_beam):
        return ShadowBeam.traceFromOE(shadow_oe, input_shadow_beam)

    def calculateIntensity(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Intensity.
        """
        shadow_beam = radiation
        #plot_mesh_x, plot_mesh_y, intensity = self._gaussianBroadenedIntensity(shadow_beam._beam.rays)

        out_dict = shadow_beam._beam.plotxy(1,3,nolost=1,nbins_h=100,nbins_v=50)

        return [out_dict['histogram'], out_dict['bin_h_left'], out_dict['bin_v_left']]

    def calculatePhase(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Phases.
        """
        raise NotImplementedError
