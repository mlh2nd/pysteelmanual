unit_systems = {"in-kip": {"length":"in", "area":"in^2", "volume":"in^3",
                           "force":"kip", "stress":"ksi", "moment":"kip-in"},
                "mm-kN": {"length":"mm", "area":"mm^2", "volume":"mm^3",
                          "force":"kN", "stress":"MPa", "moment":"kN-mm"}}


class UnitSystem():
    """Set of units for structural calculations.
    
    Units should be derived from consistent base units for length and force"""
    def __init__(self, label,
                 length: str, area: str, volume: str,
                 force: str, stress: str, moment: str,
                 unit_weight: str):
        self.label = label
        self.length = length
        self.area = area
        self.volume = volume
        self.force = force
        self.stress = stress
        self.moment = moment
        self.unit_weight = unit_weight


IN_KIP = UnitSystem(label="IN_KIP",
                    length="in", area="in^2", volume="in^3",
                    force="kip", stress="ksi", moment="kip-in",
                    unit_weight="kip/in^3")

MM_KN = UnitSystem(label="MM_KN",
                   length="mm", area="mm^2", volume="mm^3",
                   force="kN", stress="MPa", moment="kN-mm",
                   unit_weight="kN/mm^3")