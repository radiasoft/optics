"""
Minimal implementation of a SRW driver.
"""

from srwlib import *

from optics.driver.abstract_driver import AbstractDriver

from optics.beam.electron_beam_pencil import ElectronBeamPencil

from optics.magnetic_structures.undulator import Undulator
from optics.magnetic_structures.bending_magnet import BendingMagnet

from optics.beamline.optical_elements.lens.lens_ideal import LensIdeal
from optics.beamline.optical_elements.image_plane import ImagePlane

from code_drivers.SRW.SRW_adapter import SRWAdapter
from code_drivers.SRW.SRW_undulator_setting import SRWUndulatorSetting
from code_drivers.SRW.SRW_bending_magnet_setting import SRWBendingMagnetSetting
from code_drivers.SRW.SRW_beamline_component_setting import SRWBeamlineComponentSetting

class SRWDriver(AbstractDriver):

    def calculate_radiation(self,electron_beam, magnetic_structure, beamline, energy_min, energy_max):
        """
        Calculates radiation.

        :param electron_beam: ElectronBeam object
        :param magnetic_structure: Source object
        :param beamline: beamline object
        :param energy_min: Minimal energy for the calculation
        :param energy_max: Maximal energy for the calculation
        :return: SRW wavefront.
        """
        # Get position of the first component. We need this to know where to calculate the source radiation.
        first_component = beamline.component_by_index(0)
        position_first_component = beamline.position_of(first_component)

        # Instanciate an adapter.
        srw_adapter = SRWAdapter()

        # Create srw electron beam from generic electron beam.
        srw_electron_beam = srw_adapter.SRW_electron_beam(electron_beam)

        # Calculate the source radiation depending on the chosen source.
        # Only undulator here.
        # In the real driver this should be refactored to separate functions.
        if isinstance(magnetic_structure, Undulator):
            undulator = magnetic_structure

            srw_undulator = srw_adapter.magnetic_field_from_undulator(undulator)
            max_theta = undulator.gaussianCentralConeDivergence(electron_beam.gamma()) * 2.5

            z_start = undulator.length()+position_first_component.z()
            grid_length = max_theta * z_start / sqrt(2.0)

            wavefront = srw_adapter.create_quadratic_SRW_wavefront_single_energy(grid_size=1000,
                                                                            grid_length=grid_length,
                                                                            z_start=z_start,
                                                                            srw_electron_beam=srw_electron_beam,
                                                                            energy=int(undulator.resonanceEnergy(electron_beam.gamma(),0.0,0.0)))

            # Use custom settings if present. Otherwise use default SRW settings.
            if undulator.has_settings(self):
                # Mind the self in the next line.
                # It tells the DriverSettingsManager to use SRW settings.
                undulator_settings = undulator.settings(self)
            else:
                undulator_settings = SRWUndulatorSetting()
            print("SRW_driver.calculate_radiation calls CalcElecFieldSR (undulator)...")
            srwl.CalcElecFieldSR(wavefront, 0, srw_undulator, undulator_settings.toList())
            print("done in ",round(time.time() - t0), "s")
        elif isinstance(magnetic_structure, BendingMagnet):
            bending_magnet = magnetic_structure

            # Use custom settings if present. Otherwise use default SRW settings.
            if bending_magnet.has_settings(self):
                bending_magnet_settings = bending_magnet.settings(self)
            else:
                bending_magnet_settings = SRWBendingMagnetSetting()

            srw_bending_magnet = srw_adapter.magnetic_field_from_bending_magnet(bending_magnet)

            # Determine position of first optical element to calculate initial wavefront there.
            z_start = position_first_component.z()

            # Determine acceptances.
            # Horizontal
            horizontal_angle =  bending_magnet_settings.horizontal_acceptance_angle()
            horizontal_grid_length = 0.5*horizontal_angle*z_start

            # Vertical
            vertical_angle = bending_magnet_settings.vertical_acceptance_angle()
            vertical_grid_length = 0.5*vertical_angle*z_start

            # Create rectangular SRW wavefront.
            wavefront = srw_adapter.create_rectangular_SRW_wavefront(grid_size=10,
                                                                  grid_length_vertical=horizontal_grid_length,
                                                                  grid_length_horizontal=vertical_grid_length,
                                                                  z_start=z_start,
                                                                  srw_electron_beam=srw_electron_beam,
                                                                  energy_min=energy_min,
                                                                  energy_max=energy_max)

            # Calculate initial wavefront.
            print("SRW_driver.calculate_radiation calls CalcElecFieldSR (bending magnet)...")
            t0 = time.time()
            srwl.CalcElecFieldSR(wavefront, 0, srw_bending_magnet, bending_magnet_settings.to_list())
            print("done in ",round(time.time() - t0), "s")
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
            position = beamline.position_of(component)

            # Add drift space between two components.
            if position.z() > current_z_position:
                distance = position.z()-current_z_position
                srw_optical_element.append(SRWLOptD(distance))

                if component.has_settings(self):
                    component_settings = component.settings(self)

                    if component_settings.has_drift_space_settings():
                        drift_space_settings = component_settings._drift_space_settings
                    else:
                        # If there are no drift space settings use default settings.
                        drift_space_settings = SRWBeamlineComponentSetting()

                    #TODO: check this, it was inside else
                    srw_preferences.append(drift_space_settings.to_list())
                current_z_position = position.z()

            if isinstance(component, LensIdeal):
                srw_component = SRWLOptL(_Fx=component.focalX(),
                                         _Fy=component.focalY())
                srw_optical_element.append(srw_component)
            elif isinstance(component, ImagePlane):
                pass
            else:
                raise NotImplementedError

            # Use custom settings if present. Otherwise use default SRW settings.
            if component.has_settings(self):
                # Mind the self in the next line.
                # It tells the DriverSettingsManager to use SRW settings.
                component_settings = component.settings(self)
            else:
                component_settings = SRWBeamlineComponentSetting()

            srw_preferences.append(component_settings.to_list())

        # Create the srw beamline object.
        srw_beamline = SRWLOptC(srw_optical_element,
                                srw_preferences)

        # Call SRW to perform propagation.
        print("SRW_driver calls PropagElecField...")
        t0 = time.time()
        srwl.PropagElecField(wavefront, srw_beamline)
        print("done in ",round(time.time() - t0), "s")


        # TODO: Decoration of SRW wavefront with glossary object. Consider to better use a "driver results" object.
        wavefront._electron_beam = deepcopy(electron_beam)

        return wavefront

    def calculate_intensity(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Intensity.
        """
        wavefront = radiation
        mesh = deepcopy(wavefront.mesh)
        intensity = array('f', [0]*mesh.nx*mesh.ny)

        if isinstance(radiation._electron_beam, ElectronBeamPencil):
            intensity_method = 0
        else:
            intensity_method = 1

        print("SRW_driver.calculate_intensity calls CalcIntFromElecField...")
        t0 = time.time()
        srwl.CalcIntFromElecField(intensity, wavefront, 6, intensity_method, 3, mesh.eStart, 0, 0)
        print("done in ",round(time.time() - t0), "s")

        dim_x = np.linspace(mesh.xStart, mesh.xFin, mesh.nx)
        dim_y = np.linspace(mesh.yStart, mesh.yFin, mesh.ny)
        intensity = np.array(intensity).reshape((mesh.ny,mesh.nx))

        return [intensity.transpose(), dim_x, dim_y]

    def calculate_phase(self, radiation):
        """
        Calculates intensity of the radiation.
        :param radiation: Object received from self.calculateRadiation
        :return: Phases.
        """
        wavefront = radiation
        mesh = deepcopy(wavefront.mesh)

        phase = array('d', [0]*mesh.nx*mesh.ny)
        print("SRW_driver.calculate_phase calls CalcIntFromElecField...")
        t0 = time.time()
        srwl.CalcIntFromElecField(phase, wavefront, 0, 4, 3, mesh.eStart, 0, 0)
        print("done in ",round(time.time() - t0), "s")

        dim_x = np.linspace(mesh.xStart, mesh.xFin, mesh.nx)
        dim_y = np.linspace(mesh.yStart, mesh.yFin, mesh.ny)

        return [phase, dim_x, dim_y]