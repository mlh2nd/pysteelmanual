from steelpy.steelpy import Section
from .definitions.designcodes import DESIGN_CODES
from .steelcodes import aisc_360_22


unit_systems = {"in-kip": {"length":"in", "area":"in^2", "volume":"in^3",
                           "force":"kip", "stress":"ksi", "moment":"kip-in"},
                "mm-kN": {"length":"mm", "area":"mm^2", "volume":"mm^3",
                          "force":"kN", "stress":"MPa", "moment":"N-m"}}


class SteelMember():
    """
    Member class for steel design.
    """
    def __init__(self, label:str="Steel Member", 
                 code:str="aisc_360_22",
                 method:str="lrfd",
                 units:dict=unit_systems["in-kip"], 
                 section:str|Section=None, 
                 length:float=0.0,
                 force_actions:dict={},
                 design_props:dict={}):
        self.label = label
        self.code = code.lower()
        self.method = method.lower()
        self.section = section
        self.length = length
        self.units = units
        self.design_props = design_props
        self.force_actions=force_actions
        self.results = {}
        self.validate()

    def validate(self):
        if self.code not in DESIGN_CODES:
            raise ValueError(f"""Invalid design code \"{self.code}\".\n
                             Available codes: {DESIGN_CODES}""")
    
    def design_member(self):
        """
        Run member design checks and populate results dictionary.
        """
        self.results = {"Placeholder":"Results"}

    def clear_results(self):
        """
        Clear member design results.
        """
        self.results = {}
        print("Member results cleared")

    def update_member(self, section=None, length=None, units=None,
                      force_actions=None, design_props=None):
        """
        Update member parameters and clear results.
        """
        if section:
            self.section=section
        if length:
            self.length=length
        if units:
            self.units=units
        if force_actions:
            self.force_actions=force_actions
        if design_props:
            self.design_props=design_props
        self.clear_results()