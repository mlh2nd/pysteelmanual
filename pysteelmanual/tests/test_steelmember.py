from pysteelmanual import SteelMember
from pysteelmanual.units import unit_systems


def test_steelmember_methods():
    member = SteelMember("Test Member", "aisc_360_22", "lrfd", unit_systems["mm-kN"],
                         "W8X10", 1200, 
                         {"LC1":{"axial":10.5, 
                                 "major_flex":5.3}},
                         {"compression":{"Lx":1200,
                                         "Ly":600}, 
                          "major_flex":{"Lb":300}})
    
    assert member.label == "Test Member"
    assert member.code == "aisc_360_22"
    assert member.method == "lrfd"
    assert member.units["length"] == "mm"
    assert member.section == "W8X10"
    assert member.length == 1200
    assert member.force_actions["LC1"]["axial"] == 10.5
    assert member.design_props["major_flex"] == {"Lb":300}