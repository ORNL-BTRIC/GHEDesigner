from json import loads

from ghedesigner.borehole import GHEBorehole
from ghedesigner.enums import BHPipeType, TimestepType
from ghedesigner.gfunction import GFunction
from ghedesigner.ground_heat_exchangers import GHE
from ghedesigner.media import GHEFluid, Grout, Pipe, Soil
from ghedesigner.simulation import SimulationParameters
from ghedesigner.tests.test_base_case import GHEBaseTest


class TestComputedGFunctionSimAndSize(GHEBaseTest):
    def test_computed_g_function_sim_and_size(self):
        # Borehole dimensions
        # -------------------
        h = 100.0  # Borehole length (m)
        d = 2.0  # Borehole buried depth (m)
        dia = 140.0 / 1000.0  # Borehole diameter
        b = 5.0  # Borehole spacing (m)

        # Pipe dimensions
        # ---------------
        d_out = 0.04216  # Pipe outer diameter (m)
        d_in = 0.03404  # Pipe inner diameter (m)
        r_out = d_out / 2.0
        r_in = d_in / 2.0
        s = 0.01856  # Inner-tube to inner-tube Shank spacing (m)
        epsilon = 1.0e-6  # Pipe roughness (m)

        # Pipe positions
        # --------------
        # Single U-tube [(x_in, y_in), (x_out, y_out)]
        pos = Pipe.place_pipes(s, r_out, 1)
        # Single U-tube BHE object

        # Thermal conductivities
        # ----------------------
        k_p = 0.4  # Pipe thermal conductivity (W/m.K)
        k_s = 2.0  # Ground thermal conductivity (W/m.K)
        k_g = 1.0  # Grout thermal conductivity (W/m.K)

        # Volumetric heat capacities
        # --------------------------
        rho_cp_p = 1542000.0  # Pipe volumetric heat capacity (J/K.m3)
        rho_cp_s = 2343493.0  # Soil volumetric heat capacity (J/K.m3)
        rho_cp_g = 3901000.0  # Grout volumetric heat capacity (J/K.m3)

        # Thermal properties
        # ------------------
        # Pipe
        pipe = Pipe(pos, r_in, r_out, s, epsilon, k_p, rho_cp_p)
        # Soil
        ugt = 18.3  # Undisturbed ground temperature (degrees Celsius)
        soil = Soil(k_s, rho_cp_s, ugt)
        # Grout
        grout = Grout(k_g, rho_cp_g)

        # Read in g-functions from GLHEPro
        glhe_json_data = self.test_data_directory / 'GLHEPRO_gFunctions_12x13.json'
        data = loads(glhe_json_data.read_text())

        # Configure the database data for input to the geothermal gFunction object
        geothermal_g_input = GFunction.configure_database_file_for_usage(data)

        # Initialize the gFunction object
        g_function = GFunction(**geothermal_g_input)

        # Inputs related to fluid
        # -----------------------
        v_flow_system = 31.2  # System volumetric flow rate (L/s)
        # Fluid properties
        fluid = GHEFluid(fluid_str="Water", percent=0.0)

        # Define a borehole
        borehole = GHEBorehole(h, d, dia / 2.0, x=0.0, y=0.0)

        # Simulation start month and end month
        # --------------------------------
        # Simulation start month and end month
        start_month = 1
        n_years = 20
        end_month = n_years * 12
        # Maximum and minimum allowable fluid temperatures
        max_eft_allowable = 35  # degrees Celsius
        min_eft_allowable = 5  # degrees Celsius
        # Maximum and minimum allowable heights
        max_height = 200  # in meters
        min_height = 60  # in meters
        sim_params = SimulationParameters(
            start_month,
            end_month,
            max_eft_allowable,
            min_eft_allowable,
            max_height,
            min_height,
        )

        hourly_extraction_ground_loads = self.get_atlanta_loads()

        # Initialize GHE object
        ghe = GHE(
            v_flow_system,
            b,
            BHPipeType.SINGLEUTUBE,
            fluid,
            borehole,
            pipe,
            grout,
            soil,
            g_function,
            sim_params,
            hourly_extraction_ground_loads,
        )

        ghe.size(TimestepType.HYBRID)

        calculation_details = "GLHEPRO_gFunctions_12x13.json".split(".")[0]
        self.log(calculation_details)
        self.log(f"Height of boreholes: {ghe.bhe.b.H:0.3f}")
