import logging
from battery_base_V2 import BatteryBase
from lipo_battery import LiPoBatteryPack
from nmc_battery import NMCBatteryPack
from motor import Motor
from plotting_utils import plot_current_profile, plot_voltage_profile, plot_voltage_and_current_profile


class EBikeSimluator:
    """Simple simulator for a battery pack. The simulator applies a current profile to the battery pack and records the voltage profile."""

    def __init__(self, battery: BatteryBase, motor: Motor) -> None:
        self.battery = battery
        self.motor = motor

        self.voltage_profile = []
        self.current_profile = []
        self.soc_profile = []
        self.power_el_profile = []
        self.akku_warning_triggerd = False #Flag für Akkuwarnung
        self.akkutype = [] #Name des Akkutyps für Loggingmeldung
        self.batempty = False #Flag für Leere Batterie für Logging

    def simulate(self, torque_profile: list[float], duration_profile: list[float], timedt, akkutype: str) -> None:
        """In dieser Simulation wird aus dem Drehmomentprofile der Motorstrom berechnet. Dieses Stromprofil wird dann auf das Akkupack als Last angewendet."""
        self.akkutype = akkutype #Akkutyp für Logging
        self.voltage_profile.append(self.battery.voltage())
        self.soc_profile.append(self.battery.soc * 100)
        logging.info("Starte Simulation von %s", self.akkutype) #Logging für Ende der Simulation

        for m, t, d in zip(torque_profile, duration_profile, timedt):            
            current_draw = self.motor.calc_current_motor(torque_Nm=m)
            self.battery.apply_current(current=current_draw, duration=t)
            self.current_profile.append(current_draw)            
            self.voltage_profile.append(self.battery.voltage(current=current_draw))
            self.soc_profile.append(self.battery.soc * 100)
            if self.battery.soc < 0.2 and not self.akku_warning_triggerd:
                logging.warning("[Fahrtzeit: %s] Kritischer Akkustand! Akkustand vom %s ist unter 20%%", d, self.akkutype) #Loggt den kritischen Akkustand
                self.akku_warning_triggerd = True
            if  self.battery.is_empty():
                self.batempty = True

        self.power_el_profile = self.motor.calc_power_el(self.voltage_profile, self.current_profile)
        if self.batempty:
            logging.info("Simulation von %s nicht erfolgreich beendet! Akku leer!", self.akkutype) #Logging für Ende der Simulation
        else:
            logging.info("Simulation von %s erfolgreich beendet", self.akkutype) #Logging für Ende der Simulation

if __name__ == "__main__":
    torque_profile = [65.0, 32.0, 40.0, 10.0, 25.0, -10.0, 55.0, 13.0, -20.0, 18.0]
    duration_s = [300.0, 240.0, 90.0, 150.0, 120.0, 300.0, 60.0, 30.0, 120.0, 180.0]

    batterylipo = LiPoBatteryPack(capacity_nom_Ah=10)
    batterynmc = NMCBatteryPack(capacity_nom_Ah=10)
    motor = Motor()

    #simlipo = EBikeSimluator(batterylipo, motor)
    #simlipo.simulate(torque_profile, duration_s)
    #print(batterylipo)

    #simnmc = EBikeSimluator(batterynmc, motor)
    #simnmc.simulate(torque_profile, duration_s)
    #print(batterynmc)

    #plot_voltage_profile(voltage_profile=simlipo.voltage_profile, duration_profile=duration_s)
    #plot_current_profile(current_profile=simlipo.current_profile, duration_profile=duration_s)
    #plot_voltage_and_current_profile(simlipo.voltage_profile, simlipo.current_profile, duration_s)

    #input("Press Enter to exit...")