from battery_base import BatteryBase

class BatteryPack(BatteryBase):

    def __init__(
        self,
        capacity_nom_Ah: float, #Nennkapazität des Akkus
        internal_resistance_mOhm: float,
        initial_soc: float = 1.0,   #aktueller Ladestand
        Vmin: float = 3.2,
        Vmax: float = 4.2):
    
        #initial_soc wird auf 1 gesetzt, weil man bei 
        #der Simulation standartmäßig mit einem vollen Akku starten will.
        

        self.C_nom = capacity_nom_Ah * (60.0 * 60.0)    #umrechnen in SI-Einheit
        self.soc = max(0.0, min(initial_soc, 1.0))      #muss immer zwischen 0 und 1 sein
        self.R_int = internal_resistance_mOhm * 1e-3    #umrechnen in Ohm für SI_Einheiten
        self.Vmin = Vmin
        self.Vmax = Vmax
        

    def apply_current(self, current: float, duration: float) -> None:
        dsoc = -(current * duration) / self.C_nom
        self.soc = max(0.0, min(self.soc + dsoc, 1.0))

    def voltage(self, current: float = 0.0) -> float:
        U_oc = self.Vmin + self.soc * (self.Vmax - self.Vmin)   #U_oc ist open circuit voltage
        return U_oc - self.R_int * current

    def is_empty(self) -> bool:
        return self.soc <= 0.0 + 1e-9   #1e-9 wurde geschrieben, damit nicht alle nachkommastellan geschaut werden

    def is_full(self) -> bool:
        return self.soc >= 1.0 - 1e-9

    def __str__(self):
        return f"BatteryPack(SoC={self.soc * 100:.1f}%, V={self.voltage():.2f} V)"
