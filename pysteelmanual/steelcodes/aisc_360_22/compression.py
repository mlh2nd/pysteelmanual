"""
Member design per AISC 360-22 Chapter E, "Design of Members for Compression"
"""

import efficalc as ef
from pysteelmanual.units import unit_systems, UnitSystem, IN_KIP, MM_KN
from pysteelmanual.sections import RoundBar #RectBar
from pysteelmanual.materials import SteelMaterial

###########################################################################
# E1. GENERAL PROVISIONS
###########################################################################

PHI_C = 0.90    # LRFD strength reduction factor for compression
OMEGA_C = 1.67  # ASD safety factor for compression


###########################################################################
# E2. EFFECTIVE LENGTH
###########################################################################

def calc_slenderness_ratio(unbraced_length: float, 
                           radius_of_gyration: float,
                           effective_length_factor: float=1.0,
                           subscript="",
                           units: UnitSystem=IN_KIP,
                           ) -> ef.Calculation:
    """Calculate member slenderness, Lc/r = KL/r"""
    if subscript:
        length_string = f"L_{subscript}"
        k_string = f"K_{subscript}"
        r_string = f"r_{subscript}"
        ratio_string = "(\\frac{L_c}{r})_"+subscript
    else:
        length_string = "L"
        k_string = "K"
        r_string = "r"
        ratio_string = "\\frac{L_c}{r}"
    length = ef.Input(length_string, unbraced_length, units.length, 
                      "Laterally unbraced length of member")
    k_factor = ef.Input(k_string, effective_length_factor, None,
                        "Effective length factor")
    r = ef.Input(r_string, radius_of_gyration, units.length, "Radius of gyration")

    slenderness_ratio = ef.Calculation(ratio_string, 
                                       ef.brackets(k_factor * length) / r, None,
                                       "Member slenderness ratio")
    
    return slenderness_ratio


###########################################################################
# E3. FLEXURAL BUCKLING OF MEMBERS WITHOUT SLENDER ELEMENTS
###########################################################################

def calc_nominal_compressive_strength_E3(nominal_stress: float|ef.Calculation|ef.Input, 
                                         area: float,
                                         units: UnitSystem=IN_KIP,
                                         ) -> ef.Calculation:
    """Calculate nominal compressive strength per Equation E3-1.
    If Fn is entered as an Efficalc Input or Calculation, it will
    be used without restating its definition."""
    Ag = ef.Input("A_g", area, units.area,
                  "Gross sectional area")
    if isinstance(nominal_stress, ef.Calculation) or isinstance(nominal_stress, ef.Input):
        Pn = ef.Calculation("P_n", nominal_stress*Ag, units.force,
                            "Nominal compressive strength",
                            "AISC 360-22 Eq E3-1")
    else:
        Fn = ef.Input("F_n", nominal_stress, units.stress,
                      "Nominal stress")
        Pn = ef.Calculation("P_n", Fn*Ag, units.force,
                            "Nominal compressive strength",
                            "AISC 360-22 Eq E3-1")
    return Pn


def calc_nominal_flexural_buckling_stress(elastic_buckling_stress: float,
                                          yield_stress: float,
                                          units: UnitSystem=IN_KIP,
                                          ) -> ef.Calculation:
    """Calculate nominal flexural buckling stress per Equations E3-2 and E3-3"""
    Fe = ef.Input("F_e", elastic_buckling_stress, units.stress,
                  "Elastic buckling stress")
    Fy = ef.Input("F_y", yield_stress, units.stress,
                  "Yield stress")
    if Fy.result()/Fe.result() <= 2.25:
        ef.Comparison(Fy/Fe, "<=", 2.25, "\\text{Use Eq E3-2}")
        Fn = ef.Calculation("F_n", (0.658**(Fy/Fe))*Fy, units.stress,
                            "Nominal flexural buckling stress",
                            "AISC 360-22 Eq E3-2")
    else:
        ef.Comparison(Fy/Fe, ">", 2.25, "\\text{Use Eq E3-3}")
        Fn = ef.Calculation("F_n", 0.877*Fe, units.stress,
                            "Nominal flexural buckling stress",
                            "AISC 360-22 Eq E3-3")
    
    return Fn  


def calc_elastic_buckling_stress(slenderness: float, 
                                 elastic_modulus: float,
                                 units: UnitSystem=IN_KIP,
                                 ) -> ef.Calculation:
    """Calculate elastic buckling stress per Equation E3-4"""
    slenderness_ratio = ef.Input("\\frac{L_c}{r}", slenderness, None, "Member slenderness ratio")
    modulus = ef.Input("E", elastic_modulus, units.stress, "Modulus of elasticity")
    buckling_stress = ef.Calculation("F_e", ef.PI**2 * modulus / slenderness_ratio ** 2,
                                     units.stress, "Elastic buckling stress",
                                     "AISC 360-22 Eq E3-4")
    return buckling_stress


###########################################################################
# E4. TORSIONAL AND FLEXURAL-TORSIONAL BUCKLING OF SINGLE ANGLES AND
# MEMBERS WITHOUT SLENDER ELEMENTS
###########################################################################

def calc_ft_elastic_buckling_stress_doubly_symmetric(z_effective_length: float,
                                                     warping_constant: float,
                                                     Ix: float,
                                                     Iy: float,
                                                     J: float,
                                                     elastic_modulus: float,
                                                     shear_modulus: float,
                                                     units: UnitSystem=IN_KIP,
                                                     ) -> ef.Calculation:
    """Calculate torsional or flexural-torsional elastic buckling stress per Equation E4-2"""
    Lcz = ef.Input("L_{cz}", z_effective_length, units.length,
                   "Effective member length for buckling about longitudinal axis")
    E = ef.Input("E", elastic_modulus, units.stress,
                 "Modulus of elasticity")
    G = ef.Input("G", shear_modulus, units.stress,
                 "Shear modulus of elasticity")
    Cw = ef.Input("C_w", warping_constant, f"{units.length}^6",
                  "Warping constant")
    Ix = ef.Input("I_x", Ix, f"{units.length}^4",
                  "Moment of inertia about principal major axis")
    Iy = ef.Input("I_y", Iy, f"{units.length}^4",
                  "Moment of inertia about principal minor axis")
    J = ef.Input("J", J, f"{units.length}^4",
                 "Torsional constant")
    
    Fe = ef.Calculation("F_e", 
                        ef.brackets(ef.PI**2*E*Cw/Lcz**2+G*J)*(1/(Ix+Iy)),
                        units.stress,
                        "Torsional or flexural-torsional elastic buckling stress",
                        "AISC 360-22 Eq E4-2")
    
    return Fe


###########################################################################
# E5. SINGLE-ANGLE COMPRESSION MEMBERS
###########################################################################

###########################################################################
# E6. BUILT-UP MEMBERS
###########################################################################

###########################################################################
# E7. MEMBERS WITH SLENDER ELEMENTS
###########################################################################

###########################################################################
# INTEGRATION: ROUND BAR
###########################################################################

def calc_round_bar_compressive_capacity(section: RoundBar, 
                                    material: SteelMaterial,
                                    length_x: float, length_y: float,
                                    k_x: float, k_y: float,
                                    design_method: str="nominal",
                                    units: UnitSystem=IN_KIP,
                                    header_level: int=1,
                                    ) -> ef.Calculation:
    """Calculate the compressive capacity of a round bar"""
    ef.Heading("Compressive Capacity of Round Bar", header_level)
    ef.TextBlock("Following AISC 360-22")
    ef.Heading("Limiting Slenderness Ratio", header_level+1)
    ratio_x = calc_slenderness_ratio(length_x, section.rx, k_x, "x", units)
    ratio_y = calc_slenderness_ratio(length_y, section.ry, k_y, "y", units)
    slenderness = ef.Calculation("\\frac{L_c}{r}", 
                                 ef.maximum(ratio_x, ratio_y),
                                 None, "Limiting slenderness ratio for design")
    ef.Heading("Flexural Buckling Capacity", header_level+1)
    Fe = calc_elastic_buckling_stress(slenderness.result(), material.E, units)
    Fn = calc_nominal_flexural_buckling_stress(Fe.result(), material.Fy, units)
    Pn = calc_nominal_compressive_strength_E3(Fn, section.area, units)
    if design_method.lower() == "nominal":
        return Pn
    elif design_method.lower() == "lrfd":
        phi = ef.Input("\\phi_c", PHI_C, None,
                       "LRFD strength reduction factor",
                       "AISC 360-22 Sect E1")
        phiPn = ef.Calculation("\\phi_cP_n", phi*Pn, units.force,
                               "Design compressive strength")
        return phiPn
    elif design_method.lower() == "asd":
        Omega = ef.Input("\\Omega_c", OMEGA_C, None,
                         "ASD safety factor",
                         "AISC 360-22 Sect E1")
        PnOmega = ef.Calculation("P_n/\\Omega_c", Pn/Omega, units.force,
                                 "Allowable compressive strength")
        return PnOmega


def calc_round_bar_lrfd_capacity(section: RoundBar, 
                                    material: SteelMaterial,
                                    length_x: float, length_y: float,
                                    k_x: float, k_y: float,
                                    units: UnitSystem=IN_KIP,
                                    header_level: int=1,
                                    ) -> ef.Calculation:
    """Calculate the LRFD compressive capacity of a round bar"""

###########################################################################
# INTEGRATION: RECTANGULAR BAR
###########################################################################

###########################################################################
# INTEGRATION: W SECTIONS
###########################################################################