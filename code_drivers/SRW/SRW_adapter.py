"""
Wrapper for glossary objects to SRW objects.
"""
from srwlib import *

class SRWAdapter:

    def SRW_electron_beam(self, electron_beam):
        """
        Translate generic electron beam to srw "electron beam".
        """
        srw_electron_beam = SRWLPartBeam()
        srw_electron_beam.Iavg = electron_beam._current
        srw_electron_beam.partStatMom1.x = 0.0
        srw_electron_beam.partStatMom1.y = 0.0

        srw_electron_beam.partStatMom1.z = 0
        srw_electron_beam.partStatMom1.xp = 0
        srw_electron_beam.partStatMom1.yp = 0
        srw_electron_beam.partStatMom1.gamma = electron_beam.gamma()

        #2nd order statistical moments:
        srw_electron_beam.arStatMom2[0] = electron_beam._moment_xx   # <(x-x0)^2> [m^2]
        srw_electron_beam.arStatMom2[1] = electron_beam._moment_xxp  # <(x-x0)*(x'-x'0)> [m]
        srw_electron_beam.arStatMom2[2] = electron_beam._moment_xpxp # <(x'-x'0)^2>
        srw_electron_beam.arStatMom2[3] = electron_beam._moment_yy   #<(y-y0)^2>
        srw_electron_beam.arStatMom2[4] = electron_beam._moment_yyp  #<(y-y0)*(y'-y'0)> [m]
        srw_electron_beam.arStatMom2[5] = electron_beam._moment_ypyp #<(y'-y'0)^2>
        srw_electron_beam.arStatMom2[10] = electron_beam._energy_spread #<(E-E0)^2>/E0^2

        return srw_electron_beam

    def SRW_undulator(self, undulator):
        """
        Translate generic undulator to srw "undulator".
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

    def magnetic_field_from_undulator(self, undulator):
        """
        Generate srw magnetic fields.
        """
        srw_undulator = self.SRW_undulator(undulator)

        magnetic_fields = SRWLMagFldC([srw_undulator],
                                      array('d', [0]), array('d', [0]), array('d', [0]))

        return magnetic_fields

    def SRW_bending_magnet(self, bending_magnet):
        """
        Translate generic bending magnet to srw "multipole magnet".
        """
        magnetic_fields = []

        B = bending_magnet._magnetic_field
        length = bending_magnet._length

        srw_bending_magnet = SRWLMagFldM(B, 1, 'n', length)

        return srw_bending_magnet

    def magnetic_field_from_bending_magnet(self, bending_magnet):
        """
        Generate srw magnetic fields.
        """
        srw_bending_magnet = self.SRW_bending_magnet(bending_magnet)

        magnetic_fields = SRWLMagFldC([srw_bending_magnet],
                                      array('d', [0]), array('d', [0]), array('d', [0]))

        return magnetic_fields

    def create_rectangular_SRW_wavefront(self, grid_size, grid_length_vertical, grid_length_horizontal,
                                      z_start, srw_electron_beam, energy_min, energy_max):
        """
        Generates a rectangular srw wavefront.
        """
        srw_wavefront = SRWLWfr()
        srw_wavefront.allocate(1, grid_size, grid_size)
        srw_wavefront.mesh.zStart = float(z_start)
        srw_wavefront.mesh.eStart = energy_min
        srw_wavefront.mesh.eFin   = energy_max
        srw_wavefront.mesh.xStart = -grid_length_vertical
        srw_wavefront.mesh.xFin   =  grid_length_vertical
        srw_wavefront.mesh.yStart = -grid_length_horizontal
        srw_wavefront.mesh.yFin   =  grid_length_horizontal

        srw_wavefront.partBeam = srw_electron_beam

        return srw_wavefront

    def create_quadratic_SRW_wavefront_single_energy(self, grid_size, grid_length, z_start, srw_electron_beam, energy):
        """
        Generates a quadratic srw wavefront.
        """
        return self.createRectangularSRWWavefrontSingleEnergy(grid_size, grid_length, grid_length, z_start, srw_electron_beam, energy, energy)
