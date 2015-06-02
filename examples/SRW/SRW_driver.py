"""
Minimal implementation of a SRW driver.
"""
from srwlib import *


from optics.driver.abstract_driver import AbstractDriver
from optics.source.undulator import Undulator
from optics.source.bending_magnet import BendingMagnet
from optics.beamline.optical_elements.lens.lens_ideal import LensIdeal

from examples.SRW.SRW_undulator_setting import SRWUndulatorSetting
from examples.SRW.SRW_bending_magnet_setting import SRWBendingMagnetSetting
from examples.SRW.SRW_beamline_component_setting import SRWBeamlineComponentSetting

class SRWDriver(AbstractDriver):

    def _SRWElectronBeam(self, electron_beam):
        """
        Private helper function to translate generic electron beam to srw "electron beam".
        Should/could go to another file.
        """

        srw_electron_beam = SRWLPartBeam()
        srw_electron_beam.Iavg = electron_beam.averageCurrent()
        srw_electron_beam.partStatMom1.x = electron_beam.x()
        srw_electron_beam.partStatMom1.y = electron_beam.y()

        srw_electron_beam.partStatMom1.z = 0
        srw_electron_beam.partStatMom1.xp = 0
        srw_electron_beam.partStatMom1.yp = 0
        srw_electron_beam.partStatMom1.gamma = electron_beam.gamma()

        return srw_electron_beam

    def _SRWUndulator(self, undulator):
        """
        Private helper function to translate generic undulator to srw "undulator".
        Should/could go to another file.
        """

        magnetic_fields = []

        if undulator.K_vertical() > 0.0:
            vertical_field = SRWLMagFldH(1, 'v', undulator.B_vertical(), 0, 1, 1)
            magnetic_fields.append(vertical_field)

        if undulator.K_horizontal() > 0.0:
            horizontal_field = SRWLMagFldH(1, 'h', undulator.B_horizontal(), 0, -1, 1)
            magnetic_fields.append(horizontal_field)

        srw_undulator = SRWLMagFldU(magnetic_fields,
                                    undulator.periodLength(),
                                    undulator.periodNumber())

        return srw_undulator

    def _magnetFieldFromUndulator(self, undulator):
        """
        Private helper function to generate srw magnetic fields.
        Should/could go to another file.
        """

        srw_undulator = self._SRWUndulator(undulator)

        magnetic_fields = SRWLMagFldC([srw_undulator],
                                      array('d', [0]), array('d', [0]), array('d', [0]))

        return magnetic_fields

    def _SRWBendingMagnet(self, bending_magnet):
        """
        Private helper function to translate generic bending magnet to srw "multipole magnet".
        Should/could go to another file.
        """
        magnetic_fields = []

        B = bending_magnet.magneticField()
        radius = bending_magnet.radius()
    
        # TODO: do the right conversion.
        bending_magnet_length = 1.0/radius

        srw_bending_magnet = SRWLMagFldM(B, 1, 'n', bending_magnet_length)

        return srw_bending_magnet

    def _magnetFieldFromBendingMagnet(self, bending_magnet):
        """
        Private helper function to generate srw magnetic fields.
        Should/could go to another file.
        """

        srw_bending_magnet = self._SRWBendingMagnet(bending_magnet)

        magnetic_fields = SRWLMagFldC([srw_bending_magnet],
                                      array('d', [0]), array('d', [0]), array('d', [0]))

        return magnetic_fields

    def _createRectangularSRWWavefrontSingleEnergy(self, grid_size, grid_length_vertical, grid_length_horizontal, z_start, srw_electron_beam, energy):
        """
        Private helper function to translate a srw wavefront.
        """

        srw_wavefront = SRWLWfr()
        srw_wavefront.allocate(1, grid_size, grid_size)
        srw_wavefront.mesh.zStart = float(z_start)
        srw_wavefront.mesh.eStart = energy
        srw_wavefront.mesh.eFin   = energy
        srw_wavefront.mesh.xStart = -grid_length_vertical
        srw_wavefront.mesh.xFin   =  grid_length_vertical
        srw_wavefront.mesh.yStart = -grid_length_horizontal
        srw_wavefront.mesh.yFin   =  grid_length_horizontal

        srw_wavefront.partBeam = srw_electron_beam

        return srw_wavefront

    def _createQuadraticSRWWavefrontSingleEnergy(self, grid_size, grid_length, z_start, srw_electron_beam, energy):
        """
        Private helper function to translate a srw wavefront.
        """
        return self._createRectangularSRWWavefrontSingleEnergy(grid_size, grid_length, grid_length, z_start, srw_electron_beam, energy)

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

        # Create srw electron beam from generic electron beam.
        srw_electron_beam = self._SRWElectronBeam(electron_beam)

        # Calculate the source radiation depending on the chosen source.
        # Only undulator here.
        # In the real driver this should be refactored to separate functions.
        if isinstance(radiation_source, Undulator):
            undulator = radiation_source

            magFldCnt = self._magnetFieldFromUndulator(undulator)
            max_theta = undulator.gaussianCentralConeDivergence(electron_beam.gamma()) * 2.5

            z_start = undulator.length()+position_first_component.z()
            grid_length = max_theta * z_start / sqrt(2.0)

            wavefront = self._createQuadraticSRWWavefrontSingleEnergy(grid_size=1000,
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

            magFldCnt = self._magnetFieldFromBendingMagnet(bending_magnet)

            z_start = position_first_component.z()

            horizontal_angle = 0.1 #Horizontal angle [rad]
            horizontal_grid_length = 0.5*horizontal_angle*z_start #Initial horizontal position [m]

            vertical_angle = 0.02 #Vertical angle [rad]
            vertical_grid_length = 0.5*vertical_angle*z_start   #Initial vertical position [m]

            energy = 0.5*0.123984
            wavefront = self._createRectangularSRWWavefrontSingleEnergy(grid_size=1000,
                                                                        grid_length_vertical=vertical_grid_length,
                                                                        grid_length_horizontal=horizontal_grid_length,
                                                                        z_start=z_start,
                                                                        srw_electron_beam=srw_electron_beam,
                                                                        energy=energy)

            # Use custom settings if present. Otherwise use default SRW settings.
            if bending_magnet.hasSettings(self):
                bending_magnet_settings = bending_magnet.settings(self)
            else:
                bending_magnet_settings = SRWBendingMagnetSetting()

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
                srw_component= SRWLOptL(component.focalX(),
                                        component.focalY())
                srw_optical_element.append(srw_component)
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
        plot_mesh_x = [1e+06*mesh.xStart, 1e+06*mesh.xFin, mesh.nx]
        plot_mesh_y = [1e+06*mesh.yStart, 1e+06*mesh.yFin, mesh.ny]
        return [intensity, plot_mesh_x, plot_mesh_y]

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
        plot_mesh_x = [1e+06*mesh.xStart, 1e+06*mesh.xFin, mesh.nx]
        plot_mesh_y = [1e+06*mesh.yStart, 1e+06*mesh.yFin, mesh.ny]

        return [phase, plot_mesh_x, plot_mesh_y]
