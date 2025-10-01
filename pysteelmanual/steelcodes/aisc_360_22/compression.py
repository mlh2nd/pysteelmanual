"""
Member design per AISC 360-22 Chapter E, "Design of Members for Compression"
"""

import efficalc as ef
from pysteelmanual.units import unit_systems


"""
Steel design values prescribed in Section E1
"""
PHI_C = 0.90    # LRFD strength reduction factor for compression
OMEGA_C = 1.67  # ASD safety factor for compression


def calc_slenderness_ratio(unbraced_length: float, 
                           radius_of_gyration: float,
                           effective_length_factor: float=1.0,
                           units: dict=unit_systems["in-kip"]):
    """Calculate member slenderness, Lc/r = KL/r"""

    length = ef.Input("L", unbraced_length, units["length"], 
                      "Laterally unbraced length of member")
    k_factor = ef.Input("K", effective_length_factor, None,
                        "Effective length factor")
    r = ef.Input("r", radius_of_gyration, units["length"], "Radius of gyration")

    slenderness_ratio = ef.Calculation("\\frac{L_c}{r}", 
                                       ef.brackets(k_factor * length) / r, None,
                                       "Member slenderness ratio")
    
    return slenderness_ratio


def calc_elastic_buckling_stress(slenderness: float, elastic_modulus: float,
                                 units: dict=unit_systems["in-kip"]):
    """Calculate elastic buckling stress per Equation E3-4"""
    slenderness_ratio = ef.Input("\\frac{L_c}{r}", slenderness, None, "Member slenderness ratio")
    modulus = ef.Input("E", elastic_modulus, units["stress"], "Modulus of elasticity")
    buckling_stress = ef.Calculation("F_e", ef.PI**2 * modulus / slenderness_ratio ** 2,
                                     units["stress"], "Elastic buckling stress",
                                     "AISC 360-22 Eq E3-4")
    return buckling_stress