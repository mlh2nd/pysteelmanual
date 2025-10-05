from steelpy import aisc
from .units import unit_systems
from math import pi, sqrt
from pysteelmanual.units import UnitSystem, IN_KIP, MM_KN

AISC_W_SECTIONS = aisc.profiles["W_shapes"]

class RoundBar():
    """Class for round bar section object"""
    def __init__(self, diameter: float, label: str="", units: UnitSystem=IN_KIP):
        self.D = diameter
        self.R = diameter/2
        self.area = pi * self.R**2
        self.Ix = pi * self.R**4 / 4
        self.Iy = pi * self.R**4 / 4
        self.rx = sqrt(self.Ix/self.area)
        self.ry = sqrt(self.Iy/self.area)
        self.units = units
        if label:
            self.label = label
        else:
            self.label = f"{diameter}-{units.length} Ø Round Bar"


class RectBar():
    """Class for rectangular bar section object"""
    def __init__(self, width: float, height: float, units: UnitSystem=IN_KIP):
        self.b = width
        self.h = height
        self.area = width * height
        self.Ix = 1/12 * width * height**3
        self.Iy = 1/12 * height * width**3
        self.rx = sqrt(self.Ix/self.area)
        self.ry = sqrt(self.Iy/self.area)
        self.units = units