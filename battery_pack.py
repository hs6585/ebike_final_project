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
        self.history = []


    def apply_current(self, current: float, duration: float) -> None:
        dsoc = -(current * duration) / self.C_nom
        self.soc = max(0.0, min(self.soc + dsoc, 1.0))
        soc_percent = self.soc*100  #in Prozent sieht im Plot danach besser aus

        self.history.append(soc_percent)

    def voltage(self, current: float = 0.0) -> float:
        U_oc = self.Vmin + self.soc * (self.Vmax - self.Vmin)   #U_oc ist open circuit voltage
        return U_oc - self.R_int * current

    def is_empty(self) -> bool:
        return self.soc <= 0.0 + 1e-9   #1e-9 wurde geschrieben, damit nicht alle nachkommastellan geschaut werden

    def is_full(self) -> bool:
        return self.soc >= 1.0 - 1e-9

    def get_history(self) -> dict:
        #Hier wird der Verlauf der Batterie gespeichert, um danach die Daten plotten zu können
        return self.history
    
    def simulate(self, time, current):
        for i in range(1, len(time)):
            delta_t = time[i] - time[i-1]
            strom_aktuell = current[i]
            self.apply_current(strom_aktuell, delta_t)

        soc_verlauf = self.get_history()
        soc_verlauf.insert(0, 1.0)  #damit die länge der liste weiterhin richtig bleibt
        return soc_verlauf

    def __str__(self):
        return f"BatteryPack(SoC={self.soc * 100:.1f}%, V={self.voltage():.2f} V)"




if __name__ == "__main__":
    akku = BatteryPack(capacity_nom_Ah=15.0, internal_resistance_mOhm=7)

    print(f"Start: {akku}")
    print(f"Akku ist voll? {akku.is_full()}")
    print(f"Spannung bei 20 Ampere: {akku.voltage(20.0)} V")

    akku.apply_current(20.0, 60.0)
    print(f"{akku}")
    akku.apply_current(20.0, 1800.0)
    print(f"{akku}")
    print(f"Akku ist leer? {akku.is_empty()}")

    akku.apply_current(20.0, 3600.0)
    print(f"{akku}")
    print(f"Akku ist leer? {akku.is_empty()}")

    print(akku.get_history())
