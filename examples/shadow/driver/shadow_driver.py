__author__ = 'labx'
import numpy as np

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

    def _gaussianBroadenedIntensity(self, rays):
        rays_y = rays[:,0]
        rays_x = rays[:,1]
        I = np.sum(np.array([ rays[:,i]*rays[:,i] for i in [6,7,8] ]),axis=0)

        n_x = 250
        n_y = 250
        dim_x = np.linspace(rays_x.min(),rays_x.max(),n_x)
        dim_y = np.linspace(rays_y.min(),rays_y.max(),n_y)
        int_grid = np.zeros((n_x,n_y))

        sigma = min(dim_x[1]-dim_x[0],
                    dim_y[1]-dim_y[0])/2.0
        four_sigma = 4*sigma

        print("Have some patience - this is unoptimized.")
        for pos_x,pos_y,pos_int in zip(rays_x,rays_y,I):
            for i_x in range(dim_x.shape[0]):

                if np.abs(pos_x - dim_x[i_x]) > four_sigma:
                   continue
    
                for i_y in range(dim_y.shape[0]):
                   if np.abs(pos_y - dim_y[i_y]) > four_sigma:
                      continue

                   int_grid[i_x,i_y] += np.exp(-((pos_x - dim_x[i_x])**2 + (pos_y-dim_y[i_y])**2)/sigma)

        return dim_x,dim_y, int_grid

    def calculateIntensity(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Intensity.
        """
        shadow_beam = radiation
        plot_mesh_x, plot_mesh_y, intensity = self._gaussianBroadenedIntensity(shadow_beam._beam.rays)
        return [intensity, plot_mesh_x, plot_mesh_y]

    def calculatePhase(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Phases.
        """
        raise NotImplementedError
