"""
Minimal implementation of a SRW driver.
"""
import numpy as np
from srwlib import *

from optics.driver.abstract_driver import AbstractDriver
from optics.source.undulator import Undulator
from optics.source.bending_magnet import BendingMagnet

from optics.beamline.optical_elements.lens.lens_ideal import LensIdeal
from optics.beamline.optical_elements.image_plane import ImagePlane

from examples.SRW.SRW_adapter import SRWAdapter
from examples.SRW.SRW_undulator_setting import SRWUndulatorSetting
from examples.SRW.SRW_bending_magnet_setting import SRWBendingMagnetSetting
from examples.SRW.SRW_beamline_component_setting import SRWBeamlineComponentSetting

class SRWDriver(AbstractDriver):

    def calculateRadiation(self,electron_beam, radiation_source, beamline):
        """
        Calculates radiation.

        :param electron_beam: ElectronBeam object
        :param radiation_source: Source object
        :param beamline: beamline object
        :return: SRW wavefront.
        """
        # Get position of the first component. We need this to know where to calculate the source radiation.
        first_component = beamline.componentByIndex(0)
        position_first_component = beamline.positionOf(first_component)

        # Instanciate an adapter.
        srw_adapter = SRWAdapter()

        # Create srw electron beam from generic electron beam.
        srw_electron_beam = srw_adapter.SRWElectronBeam(electron_beam)

        # Calculate the source radiation depending on the chosen source.
        # Only undulator here.
        # In the real driver this should be refactored to separate functions.
        if isinstance(radiation_source, Undulator):
            undulator = radiation_source

            magFldCnt = srw_adapter.magnetFieldFromUndulator(undulator)
            max_theta = undulator.gaussianCentralConeDivergence(electron_beam.gamma()) * 2.5

            z_start = undulator.length()+position_first_component.z()
            grid_length = max_theta * z_start / sqrt(2.0)

            wavefront = srw_adapter.createQuadraticSRWWavefrontSingleEnergy(grid_size=1000,
                                                                            grid_length=grid_length,
                                                                            z_start=z_start,
                                                                            srw_electron_beam=srw_electron_beam,
                                                                            energy=int(undulator.resonanceEnergy(electron_beam.gamma(),0.0,0.0)))

            # Use custom settings if present. Otherwise use default SRW settings.
            if undulator.hasSettings(self):
                # Mind the self in the next line.
                # It tells the DriverSettingsManager to use SRW settings.
                undulator_settings = undulator.settings(self)
            else:
                undulator_settings = SRWUndulatorSetting()

            srwl.CalcElecFieldSR(wavefront, 0, magFldCnt, undulator_settings.toList())
        elif isinstance(radiation_source, BendingMagnet):
            bending_magnet = radiation_source

            magFldCnt = srw_adapter.magnetFieldFromBendingMagnet(bending_magnet)

            # Use custom settings if present. Otherwise use default SRW settings.
            if bending_magnet.hasSettings(self):
                bending_magnet_settings = bending_magnet.settings(self)
            else:
                bending_magnet_settings = SRWBendingMagnetSetting()

            # Determine position of first optical element to calculate initial wavefront there.
            z_start = position_first_component.z()

            # Determine acceptances.
            # Horizontal
            horizontal_angle =  bending_magnet_settings.horizontalAcceptanceAngle()
            horizontal_grid_length = 0.5*horizontal_angle*z_start

            # Vertical
            vertical_angle = bending_magnet_settings.verticalAcceptanceAngle()
            vertical_grid_length = 0.5*vertical_angle*z_start

            # Determine energy of the radiation.
            energy = bending_magnet.energy()

            # Create rectangular SRW wavefront.
            wavefront = srw_adapter.createRectangularSRWWavefrontSingleEnergy(grid_size=10,
                                                                              grid_length_vertical=horizontal_grid_length,
                                                                              grid_length_horizontal=vertical_grid_length,
                                                                              z_start=z_start,
                                                                              srw_electron_beam=srw_electron_beam,
                                                                              energy=energy)

            # Calculate initial wavefront.
            srwl.CalcElecFieldSR(wavefront, 0, magFldCnt, bending_magnet_settings.toList())
        else:
            raise NotImplementedError

        # Create the srw beamline.
        srw_optical_element = list()
        srw_preferences = list()

        # Iterate over all beamline components and translate them.
        # Translate free space between two components to drift space.
        # Only lenses implemented.
        # In the real driver this should be refactored to separate functions.
        current_z_position = position_first_component.z()
        for component in beamline:
            position = beamline.positionOf(component)

            # Add drift space between two components.
            if position.z() > current_z_position:
                distance = position.z()-current_z_position
                srw_optical_element.append(SRWLOptD(distance))
                srw_preferences.append(SRWBeamlineComponentSetting().toList())
                current_z_position = position.z()

            if isinstance(component, LensIdeal):
                srw_component = SRWLOptL(_Fx=component.focalX(),
                                         _Fy=component.focalY())
                srw_optical_element.append(srw_component)
            elif isinstance(component, ImagePlane):
                continue
            else:
                raise NotImplementedError

            # Use custom settings if present. Otherwise use default SRW settings.
            if component.hasSettings(self):
                # Mind the self in the next line.
                # It tells the DriverSettingsManager to use SRW settings.
                component_settings = component.settings(self)
            else:
                component_settings = SRWBeamlineComponentSetting()

            srw_preferences.append(component_settings.toList())

        # Create the srw beamline object.
        srw_beamline = SRWLOptC(srw_optical_element,
                                srw_preferences)

        # Call SRW to perform propagation.
        srwl.PropagElecField(wavefront, srw_beamline)

        return wavefront

    def calculateIntensity(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Intensity.
        """
        wavefront = radiation
        mesh = deepcopy(wavefront.mesh)
        intensity = array('f', [0]*mesh.nx*mesh.ny)
        srwl.CalcIntFromElecField(intensity, wavefront, 6, 0, 3, mesh.eStart, 0, 0)
        dim_x = np.linspace(1e+06*mesh.xStart, 1e+06*mesh.xFin, mesh.nx)
        dim_y = np.linspace(1e+06*mesh.yStart, 1e+06*mesh.yFin, mesh.ny)
        intensity = np.array(intensity).reshape((mesh.ny,mesh.nx))
        return [intensity.transpose(), dim_x, dim_y]

    def calculatePhase(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Phases.
        """
        wavefront = radiation
        mesh = deepcopy(wavefront.mesh)

        phase = array('d', [0]*mesh.nx*mesh.ny)
        srwl.CalcIntFromElecField(phase, wavefront, 0, 4, 3, mesh.eStart, 0, 0)
        dim_x = np.linspace(1e+06*mesh.xStart, 1e+06*mesh.xFin, mesh.nx)
        dim_y = np.linspace(1e+06*mesh.yStart, 1e+06*mesh.yFin, mesh.ny)

        return [phase, dim_x, dim_y]