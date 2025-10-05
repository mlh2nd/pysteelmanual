from pysteelmanual.units import unit_systems
from pysteelmanual.units import UnitSystem, IN_KIP, MM_KN

class SteelMaterial():
    """Class to hold steel material properties"""
    def __init__(self, yield_stress: float,
                 ultimate_stress: float,
                 elastic_modulus: float=None,
                 shear_modulus: float=None,
                 unit_weight: float=None,
                 units: UnitSystem=IN_KIP):
        self.Fy = yield_stress
        self.Fu = ultimate_stress
        if elastic_modulus:
            self.E = elastic_modulus
        elif units == IN_KIP:
            self.E = 29000 # ksi
        elif units == MM_KN:
            self.E = 200000 # MPa
        if shear_modulus:
            self.G = shear_modulus
        elif units == IN_KIP:
            self.G = 11200 # ksi
        elif units == MM_KN:
            self.G = 77200 # MPa
        if unit_weight:
            self.gamma = unit_weight
        elif units == IN_KIP:
            self.gamma = 0.000284 # kip/in^3
        elif units == MM_KN:
            self.gamma = 7.85e-8 # kN/mm^3
        self.units = units


ASTM_A36 = SteelMaterial(yield_stress=36, ultimate_stress=58)
ASTM_A572_GR_50 = SteelMaterial(yield_stress=50, ultimate_stress=65)
ASTM_A992_GR_50 = SteelMaterial(yield_stress=50, ultimate_stress=65)
