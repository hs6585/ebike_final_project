from battery_pack_V2 import BatteryPack

class NMCBatteryPack(BatteryPack):

    def __init__(
        self,
        capacity_nom_Ah: float,
        internal_resistance_mOhm: float = 70.0, #10 Zellen in Serie
        initial_soc = 1.0,
        Vmin = 32.0,    #10 Zellen in Serie
        Vmax = 42.0,
        cells_in_parallel: int = 1):

        super().__init__(capacity_nom_Ah, internal_resistance_mOhm = internal_resistance_mOhm, initial_soc = initial_soc, Vmin = Vmin, Vmax = Vmax, cells_in_parallel = cells_in_parallel)

        #Werte aus den Tabellen:
        self.list_soc = [0.00, 0.04, 0.09, 0.13, 0.17, 0.21, 0.26, 0.30, 0.40, 0.52, 0.64, 0.76, 0.88, 1.00]
        self.list_uoc = [32.00, 32.61, 33.17, 33.85, 34.24, 34.66, 35.39, 35.65, 36.65, 37.64, 38.91, 40.14, 41.08, 42.00]

    def voltage(self, current: float=0.0) -> float:
        #Nun sucht man nach zwei Nachbarwerte in der Liste, umd danach zwischen 
        #diesen Punkte die Steigung zu berechnen:

        for i in range(len(self.list_soc) - 1):
            if self.list_soc[i] <= self.soc <= self.list_soc[i+1]:
                x_0 = self.list_soc[i]
                x_1 = self.list_soc[i+1]
                y_0 = self.list_uoc[i]
                y_1 = self.list_uoc[i+1]
                break       #sobald man die Nachbarn gefunden hat kann man stoppen
        
        if x_0 != x_1:      #Steigung berechnen und schauen dass der Nenner nicht 0 ist.
            steigung = (y_1 - y_0) / (x_1 - x_0)
            open_circuit_voltage = y_0 + steigung * (self.soc - x_0)     #f(t) = f_0 + a*x(t)
        else:
            open_circuit_voltage = y_0

        return open_circuit_voltage - self.R_int * current
    
if __name__ == "__main__":
    nmc_akku = NMCBatteryPack(capacity_nom_Ah=15.0, cells_in_parallel=3)
    print(f"Start: {nmc_akku}")
    nmc_akku.apply_current(70,300)
    print(f"Spannung bei 20 Ampere: {nmc_akku.voltage(20.0)} V")
    print(nmc_akku)
    