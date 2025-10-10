from steelpy.steelpy import Section
from .definitions.designcodes import DESIGN_CODES
from .steelcodes import aisc_360_22
from .units import UnitSystem, IN_KIP
from .materials import SteelMaterial
from .sections import SteelSection


class SteelMember():
    """
    Member class for steel design.
    """
    def __init__(self, 
                 label:str, 
                 section:str|SteelSection=None, 
                 material:SteelMaterial=None,
                 length:float=0.0,
                 design_code:str="aisc_360_22",
                 design_method:str="lrfd",
                 units:UnitSystem=IN_KIP, 
                 force_actions:dict={},
                 design_props:dict={}):
        self.label = label
        self.design_code = design_code.lower()
        self.design_method = design_method.lower()
        self.section = section
        self.material = material
        self.length = length
        self.units = units
        self.design_props = design_props
        self.force_actions=force_actions
        self.results = {}
        self.validate()

    def validate(self):
        if self.design_code not in DESIGN_CODES:
            raise ValueError(f"""Invalid design code \"{self.design_code}\".\n
                             Available codes: {DESIGN_CODES}""")
        if (self.section.units != self.units or
            self.material.units != self.units):
            raise ValueError(f"Incompatible unit systems:\n\
                                Member units: {self.units.label}\n\
                                Section units: {self.section.units.label}\n\
                                Material units: {self.material.units.label}\n\
                                All components must use same unit system.")
    
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