from battery_pack import BatteryPack

class LiPoBatteryPack(BatteryPack):

    def __init__(
        self,
        capacity_nom_Ah: float,
        internal_resistance_mOhm: float = 80.0, #10 Zellen in Serie
        initial_soc = 1.0,
        Vmin = 32.0,    #10 Zellen in Serie
        Vmax = 42.0):

        super().__init__(capacity_nom_Ah, internal_resistance_mOhm = internal_resistance_mOhm, initial_soc = initial_soc, Vmin = Vmin, Vmax = Vmax)

        self.list_soc = [0.00, 0.04, 0.09, 0.13, 0.17, 0.21, 0.26, 0.30, 0.40, 0.52, 0.64, 0.76, 0.88, 1.00]
        self.list_uoc = [32.00, 35.87, 36.85, 37.56, 37.87, 38.28, 38.81, 39.05, 39.55, 40.27, 40.70, 41.16, 41.65, 42]

    def voltage(self, current: float=0.0) -> float:
        current_soc = max(0.0, min(self.soc, 1.0))  #aus VO-Unterlagen

        #Nun sucht man nach zwei Nachbarwerte in der Liste, umd danach zwischen 
        #diesen Punkte die Steigung zu berechnen:

        for i in range(len(self.list_soc) - 1):
            if self.list_soc[i] <= current_soc <= self.list_soc[i+1]:
                x_0 = self.list_soc[i]
                x_1 = self.list_soc[i+1]
                y_0 = self.list_uoc[i]
                y_1 = self.list_uoc[i+1]
                break       #sobald man die Nachbarn gefunden hat kann man stoppen
        
        if x_0 != x_1:      #Steigung berechnen und schauen dass der Nenner nicht 0 ist.
            steigung = (y_1 - y_0) / (x_1 - x_0)
            U_oc = y_0 + steigung * (current_soc - x_0)     #f(t) = f_0 + a*x(t)
        else:
            U_oc = y_0

        return U_oc - self.R_int * current
    
if __name__ == "__main__":
    lipo_akku = LiPoBatteryPack(capacity_nom_Ah=15.0)

    print(f"Start: {lipo_akku}")
    print(f"Spannung bei 20 Ampere: {lipo_akku.voltage(20.0)} V")
