from battery_base_V2 import BatteryBase

class BatteryPack(BatteryBase):
    def __init__(
        self,
        capacity_nom_Ah: float,
        internal_resistance_mOhm: float = 80.0,
        initial_soc: float = 1.0,
        Vmin: float = 3.0,
        Vmax: float = 4.2,
    ):

        self.C_nom_Ah = capacity_nom_Ah
        self.C_nom = capacity_nom_Ah * (60.0 * 60.0)
        self.soc = max(0.0, min(initial_soc, 1.0))
        self.R_int = internal_resistance_mOhm * 1e-3
        self.Vmin = Vmin
        self.Vmax = Vmax

    def apply_current(self, current: float, duration: float) -> None:
        dsoc = -(current * duration) / self.C_nom
        self.soc = max(0.0, min(self.soc + dsoc, 1.0))

    def voltage(self, current: float = 0.0) -> float:
        open_circuit_voltage = self.Vmin + self.soc * (self.Vmax - self.Vmin)
        return open_circuit_voltage - self.R_int * current

    def is_empty(self) -> bool:
        return self.soc <= 0.0 + 1e-9

    def is_full(self) -> bool:
        return self.soc >= 1.0 - 1e-9

    def __str__(self):
        return f"BatteryPack(SoC={self.soc * 100:.1f}%, V={self.voltage():.2f} V)"

if __name__ == "__main__":
    akku = BatteryPack(capacity_nom_Ah=20)
    print(akku)