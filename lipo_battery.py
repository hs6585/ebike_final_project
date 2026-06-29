from battery_pack import BatteryPack

class LiFePO4BatteryPack(BatteryPack):

    def __init__(
        self,
        capacity_nom_Ah: float,
        internal_resistance_mOhm: float = 80.0, #10 Zellen in Serie
        initial_soc = 1.0,
        Vmin = 32.0,    #10 Zellen in Serie
        Vmax = 42.0):

        super().__init__(capacity_nom_Ah, internal_resistance_mOhm = internal_resistance_mOhm, initial_soc = initial_soc, Vmin = Vmin, Vmax = Vmax)

    def voltage(self, current: float=0.0) -> float:
        U_oc = self.Vmin + (self.soc**0.3) * (self.Vmax - self.Vmin)
        return U_oc - self.R_int * current