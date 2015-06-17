__author__ = 'labx'
import numpy
import Shadow

# Import elements from common Glossary
from optics.driver.abstract_driver import AbstractDriver

from optics.magnetic_structures.bending_magnet import BendingMagnet

from optics.beamline.beamline_position import BeamlinePosition

from optics.beamline.optical_elements.lens.lens_ideal import LensIdeal
from optics.beamline.optical_elements.image_plane import ImagePlane

from code_drivers.shadow.driver.shadow_beam import ShadowBeam
from code_drivers.shadow.sources.shadow_bending_magnet import ShadowBendingMagnet, ShadowBendingMagnetSetting


class ShadowDriver(AbstractDriver):

    def processSource(self, source):
        return self.traceFromSource(source)

    def processComponent(self, beamline_component, previous_result):
        return self.traceFromOE(beamline_component, previous_result)

    def calculateRadiation(self,electron_beam, magnetic_structure, beamline):
        """
        Calculates radiation.

        :param electron_beam: ElectronBeam object
        :param magnetic_structure: Source object
        :param beamline: Beamline object
        :return: ShadowBeam.
        """

        if isinstance(magnetic_structure, BendingMagnet):

            # If BendingMagnet is not configured for shadow add default settings.
            if not magnetic_structure.hasSettings(ShadowDriver()):
                magnetic_structure.addSettings(ShadowBendingMagnetSetting())

            # Create a ShadowSource for shadow API.
            shadow_source = ShadowBendingMagnet(electron_beam, magnetic_structure)
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

                #
                # we define the LensIdeal in Shadow as an ideal focusing element that
                # is implemented as an ellipsoidal morror if focalX=focalY or as
                # a toroidal mirror if focalX!=focalY
                #
                q = position_next_component.z() - position.z()
                q *= 100.0 # to cm

                p = position.z() - position_previous_component.z()
                p *= 100.0 # to cm


                shadow_oe.HOLO_W = 4879.85986
                shadow_oe.NCOL = 0
                shadow_oe.R_LAMBDA = 5000.0
                shadow_oe.T_IMAGE = q
                shadow_oe.T_INCIDENCE = 45.0   #45 degrees incident angle
                shadow_oe.T_REFLECTION = 45.0  #45 degrees incident angle
                shadow_oe.T_SOURCE = p
                if component.focalY() == component.focalX():
                    #Ellipsoidal mirror in autofocus
                    shadow_oe.FMIRR = 2
                    shadow_oe.F_DEFAULT = 0
                    shadow_oe.SIMAG = 2*component.focalY()*100.0  # Shadow units in cm
                    shadow_oe.SSOUR = 2*component.focalY()*100.0  # Shadow units in cm
                    shadow_oe.THETA = 45.0
                else:
                    #raise NotImplementedError
                    #Toroidal mirror
                    #Y meridional focusing (1/f)=(1/p)+(1/q)=2/(Rmer*cos(theta))
                    # Rmer = 2 f / cos(theta)

                    #X meridional focusing (1/f)=(1/p)+(1/q)=2cos(theta)/Rsag
                    # Rsag = 2 f cos(theta)
                    shadow_oe.FMIRR = 3
                    shadow_oe.F_EXT = 1
                    shadow_oe.F_DEFAULT = 0

                    shadow_oe.R_MAJ = 200*component.focalY()/numpy.cos(45.0*numpy.pi/180)  # Shadow units in cm
                    shadow_oe.R_MIN = 200*component.focalY()*numpy.cos(45.0*numpy.pi/180)  # Shadow units in cm
                    # Rmer = 2/numpy.cos(45*numpy.pi/180)/(1/p+1/q)
                    # Rsag = 2*numpy.cos(45*numpy.pi/180)/(1/p+1/q)
                    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>",shadow_oe.R_MAJ,shadow_oe.R_MIN,Rmer,Rsag)



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
