from math import isclose
import pysteelmanual.steelcodes.aisc_360_22.compression as comp
from pysteelmanual.units import unit_systems


def test_calc_slenderness_ratio():
    L1 = 144.5
    r1 = 2.0

    L2 = 166
    r2 = 1.6
    K2 = 0.8

    assert comp.calc_slenderness_ratio(L1, r1).result() == 72.25
    assert comp.calc_slenderness_ratio(L2, r2, K2).result() == 83.0


def test_calc_elastic_buckling_stress():
    assert isclose(comp.calc_elastic_buckling_stress(68.5, 29000), 60.99814111)
    assert isclose(comp.calc_elastic_buckling_stress(145, 29000), 13.61324745)