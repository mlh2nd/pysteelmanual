"""
Member design per AISC 360-22 Chapter F, "Design of Members for Flexure"
"""
import efficalc as ef
from pysteelmanual.sections import RoundBar
from pysteelmanual.materials import SteelMaterial
from pysteelmanual.units import UnitSystem, IN_KIP

###########################################################################
# F1. GENERAL PROVISIONS
###########################################################################

PHI_B = 0.90    # LRFD strength reduction factor for flexure
OMEGA_B = 1.67  # ASD safety factor for flexure

###########################################################################
# F11. RECTANGULAR BARS AND ROUNDS
###########################################################################

def calc_round_bar_plastic_moment(section: RoundBar,
                                  material: SteelMaterial,
                                  units: UnitSystem=IN_KIP,
                                  ) -> ef.Calculation:
    """Calculate plastic moment of round bar per Equation F11-2"""
    Fy = ef.Input("F_y", material.Fy, units.stress, "Yield stress")
    Sx = ef.Input("S_x", section.Sx, units.volume, "Elastic section modulus")
    Z = ef.Input("Z", section.Zx, units.volume, "Plastic section modulus")
    Mp = ef.Calculation("M_p", ef.minimum(Fy*Z, 1.6*Fy*Sx), units.moment,
                        "Plastic moment", "AISC 360-22 Eq F11-2")
    Mn = ef.Calculation("M_n", Mp, units.moment, "Nominal flexural strength")
    return Mn


###########################################################################
# INTEGRATION: ROUND BARS
###########################################################################

def calc_round_bar_flexural_capacity(section: RoundBar,
                                     material: SteelMaterial,
                                     design_method: str="nominal",
                                     units: UnitSystem=IN_KIP,
                                     ) -> ef.Calculation:
    """Calculate flexural capacity of round bar"""
    Mn = calc_round_bar_plastic_moment(section, material, units)

    if design_method.lower() == "nominal":
        return Mn
    elif design_method.lower() == "lrfd":
        phi = ef.Input("\\phi_b", PHI_B, None, 
                       "LRFD strength reduction factor", "AISC 360-22 Sect F1")
        phiMn = ef.Calculation("\\phi_bM_n", phi*Mn, units.moment, "Design flexural strength")
        return phiMn
    elif design_method.lower() == "asd":
        Omega = ef.Input("\\Omega_b", OMEGA_B, None,
                         "ASD safety factor", "AISC 360-22 Sect F1")
        Mn_Omega = ef.Input("M_n/\\Omega_b", Mn/Omega, units.moment, "Allowable flexural strength")
        return Mn_Omega