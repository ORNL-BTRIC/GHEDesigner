import unittest

from ghedesigner.borehole import GHEBorehole
from ghedesigner.borehole_heat_exchangers import SingleUTube
from ghedesigner.media import GHEFluid, Pipe, Grout, Soil
from ghedesigner.radial_numerical_borehole import RadialNumericalBH


class TestRadialNumericalBorehole(unittest.TestCase):

    def test_calc_sts_g_functions(self):
        fluid = GHEFluid(fluid_str='WATER', percent=0)
        borehole = GHEBorehole(height=100.0, buried_depth=2.0, radius=0.075, x=0.0, y=0.0)
        grout = Grout(k=2.0, rho_cp=2000000.0)

        r_out = 0.02667 / 2.0
        r_in = 0.0216 / 2.0
        shank_spacing = 0.0323
        roughness = 1e-6
        k_pipe = 0.4
        rho_cp_pipe = 1542000
        pipe_positions = Pipe.place_pipes(0.02, r_out, 1)
        pipe = Pipe(pipe_positions, r_in, r_out, shank_spacing, roughness, k_pipe, rho_cp_pipe)
        soil = Soil(k=2.0, rho_cp=3901000, ugt=20)
        m_dot_bh = 0.2
        bh = SingleUTube(m_dot_bh, fluid, borehole, pipe, grout, soil)
        rn_bh = RadialNumericalBH(bh)
        rn_bh.calc_sts_g_functions(bh)
