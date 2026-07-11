import logging
logging.basicConfig(format="%(asctime)s: %(levelname)s: %(message)s", #Logging
                    level=logging.INFO,
                    filename="simulation.log",
                    filemode='w')

import readGPSdata as gps
from calc_data_from_gps import CalcDataFromGPS
from motor import Motor
from lipo_battery import LiPoBatteryPack
from nmc_battery import NMCBatteryPack
from ebike_simulator import EBikeSimluator
import plots
import plot_height_map
import study
import numpy as np
import matplotlib.pyplot as plt

csv_file = "final_project_input_data.csv" #CSV-Datei mit GPS-Messdatensatz
data_dict = gps.load_and_process_data(csv_file) #Dictionary mit GPS-Daten als float

logging.info("Eingelesener GPS-Datensatz: %s", csv_file) #Logging für CSV-Datei

gpsdata = CalcDataFromGPS(data_dict) #Initialisierung der Klasse CalcDataFromGPS
distance = gpsdata.calculate_distance() #Strecke in m       
velocity = gpsdata.calculate_speed() #Geschwindigkeit in m/s
velocity_kmh = gpsdata.calculate_speed() * 3.6
accelearation = gpsdata.calculate_acceleration() #Beschleunigung in m/s^2
incline_angle = gpsdata.calculate_incline_angle() #Steigungswinkel in °
rho = gpsdata.calculate_air_density()
drag_force = gpsdata.calculate_drag_force(rho, 0.5625) #Luftwiderstandskraft in N       
driving_force = gpsdata.calculate_driving_force() #Antriebskraft in N
compass_direction = gpsdata.calculate_compass_direction() #Himmelsrichtung

elevation = gpsdata.data_dict["ele"] #Höhenprofil
time = gpsdata.data_dict["time"] #Zeitprofil in Sekunden
timedt = gpsdata.data_dict["timedt"] #Zeitprofil als Timestamp
temp = gpsdata.data_dict["temp"] #Temperatur

#Motor
motor = Motor() #Initialisierung der Klasse Motor
power_mech = motor.calc_power_mech(driving_force, velocity) #Mechanisches Leistungsprofil in W
torque = motor.calc_torque(driving_force) #Drehmoment in Nm

lipo = "Lipo-Batterypack"
nmc = "Nmc-Batterypack"

#Batterie:
battery_lipo = LiPoBatteryPack(capacity_nom_Ah=10, cells_in_parallel=3) #Batterypack mit lipo Zellen 
battery_nmc = NMCBatteryPack(capacity_nom_Ah=20, cells_in_parallel=2) #Batterypack mit nmc Zellen

logging.info("Setup Simulation: %s(%sWh), %s(%sWh)", lipo, round(battery_lipo.C_nom_Ah * battery_lipo.voltage(0)), nmc, round(battery_nmc.C_nom_Ah * battery_nmc.voltage(0))) #Loggt die Ausgangsleistung der beiden Akkus mit

#Simulation:
sim_lipo = EBikeSimluator(battery_lipo, motor) #Simulations Klasse für Lipo-Akkupack initialisieren
sim_nmc = EBikeSimluator(battery_nmc, motor) #Simulations Klasse für Nmc-Akkupack initialisieren

duration_profile = np.diff(time)# Delta Time Profile berechnen
sim_lipo.simulate(torque, duration_profile, timedt, lipo) #Simulation für Lipo-Akkupack
sim_nmc.simulate(torque, duration_profile, timedt, nmc) #Simulation für Nmc-Akkupack

logging.info("Restakku: %s(%s%%), %s(%s%%)", lipo, round(battery_lipo.soc*100, 2), nmc, round(battery_nmc.soc*100, 2)) #Logging für Restakku

h, m = gpsdata.calculate_total_time() #Berechnet Stunden und Minuten der Gesamtfahrtzeit 
logging.info("Gesamtfahrzeit: %sh%smin", h, m) #Logging für Gesamtzeit

totaldis = gpsdata.calculate_total_dis() #Berechnet die totale Distanz
logging.info("Zurueckgelegte Strecke: %skm", totaldis) #Logging für Gesamtstrecke

vm = gpsdata.calculate_vm() #Berechnet die mittlere Geschwindigkeit
logging.info("Mittlere Geschwindigkeit: %sm/s", vm) #Logging für mittlere Geschwindigkeit     

asc, des = gpsdata.calculate_asc_des() #Berechnet den Anstieg und Abstieg 
logging.info("Hoehenmeter: Aufstieg(%sm), Abstieg:(%sm)", asc, des) #Logging für Höhenmeter Anstieg und Abstieg

maxpow = gpsdata.calculate_maxpow(power_mech) #Berechnet die maximale mechanische Leistung. Es wird nur 99% angeschaut die 1% der Spitzen werden dabei vernachlässigt.
logging.info("Maximale Leistung: %sW", maxpow) #Logging für maximale Leistung

#Plots
plots.height_profile(timedt, elevation) #Höhenprofil alleine
plots.velocity_height_profile(timedt, elevation, velocity_kmh)  #Geschwindigkeits und Höhenverlauf übereinander

plots.height_power_profile(timedt[:-1], elevation[:-1], sim_lipo.power_el_profile, lipo) #Leistungs -und Höhenverlauf eines Lipoakkus plotten
plots.height_power_profile(timedt[:-1], elevation[:-1], sim_nmc.power_el_profile, nmc) #Leistungs -und Höhenverlauf eines Nmcakkus plotten

plots.soc_profile(timedt, elevation, sim_lipo.soc_profile, lipo) #Lade -und Höhenverlauf eines Lipoakkus plotten
plots.soc_profile(timedt, elevation, sim_nmc.soc_profile, nmc) #Lade -und Höhenverlauf eines Nmcakkus plotten

plot_height_map.height_map(data_dict, compass_direction)   #Die Höhenkarte über die Fahrt
plots.plot_air_density(timedt, elevation, rho)

durations_in_seconds = np.diff(timedt) / np.timedelta64(1, 's')
plots.plot_voltage_and_current_profile(sim_lipo.voltage_profile, sim_lipo.current_profile, durations_in_seconds, lipo) #Spannungs und Stromverlauf über die Zeit plotten (lipo)
plots.plot_voltage_and_current_profile(sim_nmc.voltage_profile, sim_nmc.current_profile, durations_in_seconds, nmc) #Spannungs und Stromverlauf über die Zeit plotten (nmc)

#Studie Radradius aus study.py
study.wheel_study(data_dict, 13.5, 17)    #13.5 = standard radius und 17 = beliebiger Radius für Studie

#damit alle Plots gleichzeitig öffnen und man sie mit esc wieder schließen kann
def close_all_plots(event):
    if event.key == 'escape':
        plt.close('all')

for fig_num in plt.get_fignums():
    fig = plt.figure(fig_num)
    fig.canvas.mpl_connect('key_press_event', close_all_plots)

plt.show()






