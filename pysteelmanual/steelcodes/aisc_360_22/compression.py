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
                           units: dict=unit_systems["in-kip"],
                           ) -> ef.Calculation:
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


def calc_nominal_compressive_strength_E3(nominal_stress: float, 
                                         area: float,
                                         units: dict=unit_systems["in-kip"],
                                         ) -> ef.Calculation:
    """Calculate nominal compressive strength per Equation E3-1"""
    Fn = ef.Input("F_n", nominal_stress, units["stress"],
                  "Nominal stress")
    Ag = ef.Input("A_g", area, units["area"],
                  "Gross sectional area")
    Pn = ef.Calculation("P_n", Fn*Ag, units["force"])
    return Pn


def calc_nominal_flexural_buckling_stress(elastic_buckling_stress: float,
                                          yield_stress: float,
                                          units: dict=unit_systems["in-kip"],
                                          ) -> ef.Calculation:
    """Calculate nominal flexural buckling stress per Equations E3-2 and E3-3"""
    Fe = ef.Input("F_e", elastic_buckling_stress, units["stress"],
                  "Elastic buckling stress")
    Fy = ef.Input("F_y", yield_stress, units["stress"],
                  "Yield stress")
    if Fy.result()/Fe.result() <= 2.25:
        ef.Comparison(Fy/Fe, "<=", 2.25, "\\text{Use Eq E3-2}")
        Fn = ef.Calculation("F_n", (0.658**(Fy/Fe))*Fy, units["stress"],
                            "Nominal flexural buckling stress",
                            "AISC 360-22 Eq E3-2")
    else:
        ef.Comparison(Fy/Fe, ">", 2.25, "\\text{Use Eq E3-3}")
        Fn = ef.Calculation("F_n", 0.877*Fe, units["stress"],
                            "Nominal flexural buckling stress",
                            "AISC 360-22 Eq E3-3")
    
    return Fn  


def calc_elastic_buckling_stress(slenderness: float, 
                                 elastic_modulus: float,
                                 units: dict=unit_systems["in-kip"],
                                 ) -> ef.Calculation:
    """Calculate elastic buckling stress per Equation E3-4"""
    slenderness_ratio = ef.Input("\\frac{L_c}{r}", slenderness, None, "Member slenderness ratio")
    modulus = ef.Input("E", elastic_modulus, units["stress"], "Modulus of elasticity")
    buckling_stress = ef.Calculation("F_e", ef.PI**2 * modulus / slenderness_ratio ** 2,
                                     units["stress"], "Elastic buckling stress",
                                     "AISC 360-22 Eq E3-4")
    return buckling_stress


def calc_ft_elastic_buckling_stress_doubly_symmetric(z_effective_length: float,
                                                     warping_constant: float,
                                                     Ix: float,
                                                     Iy: float,
                                                     J: float,
                                                     elastic_modulus: float,
                                                     shear_modulus: float,
                                                     units: dict=unit_systems["in-kip"],
                                                     ) -> ef.Calculation:
    """Calculate torsional or flexural-torsional elastic buckling stress per Equation E4-2"""
    Lcz = ef.Input("L_{cz}", z_effective_length, units["length"],
                   "Effective member length for buckling about longitudinal axis")
    E = ef.Input("E", elastic_modulus, units["stress"],
                 "Modulus of elasticity")
    G = ef.Input("G", shear_modulus, units["stress"],
                 "Shear modulus of elasticity")
    Cw = ef.Input("C_w", warping_constant, f"{units["length"]}^6",
                  "Warping constant")
    Ix = ef.Input("I_x", Ix, f"{units["length"]}^4",
                  "Moment of inertia about principal major axis")
    Iy = ef.Input("I_y", Iy, f"{units["length"]}^4",
                  "Moment of inertia about principal minor axis")
    J = ef.Input("J", J, f"{units["length"]}^4",
                 "Torsional constant")
    
    Fe = ef.Calculation("F_e", 
                        ef.brackets(ef.PI**2*E*Cw/Lcz**2+G*J)*(1/(Ix+Iy)),
                        units["stress"],
                        "Torsional or flexural-torsional elastic buckling stress",
                        "AISC 360-22 Eq E4-2")
    
    return Fe