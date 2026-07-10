import logging
logging.basicConfig(format="%(asctime)s: %(filename)s: %(levelname)s: %(message)s", #Logging
                    level=logging.INFO,
                    filename="simulation.log",
                    filemode='w')

import readGPSdata as gps
from calc_data_from_gps import CalcDataFromGPS
from motor import Motor
from lipo_battery import LiPoBatteryPack
from nmc_battery import NMCBatteryPack
import plots
import plot_height_map
import study

csv_file = "final_project_input_data.csv" #CSV-Datei mit GPS-Messdatensatz
data_dict = gps.load_and_process_data(csv_file) #Dictionary mit GPS-Daten als float

logging.info("Eingelesener GPS-Datensatz: %s", csv_file) #Logging für CSV-Datei

gpsdata = CalcDataFromGPS(data_dict) #Initialisierung der Klasse CalcDataFromGPS
distance = gpsdata.calculate_distance() #Strecke in m       
velocity = gpsdata.calculate_speed() #Geschwindigkeit in m/s
velocity_kmh = gpsdata.calculate_speed() * 3.6
accelearation = gpsdata.calculate_acceleration() #Beschleunigung in m/s^2
incline_angle = gpsdata.calculate_incline_angle() #Steigungswinkel in °
drag_force = gpsdata.calculate_drag_force() #Luftwiderstandskraft in N       
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
current = motor.calc_current_motor(torque) #Motorstrom in A

lipo = "Lipo-Batterypack"
nmc = "Nmc-Batterypack"

#Batterie:
battery_lipo = LiPoBatteryPack(capacity_nom_Ah=30) #Batterypack mit lipo Zellen 
battery_nmc = NMCBatteryPack(capacity_nom_Ah=30) #Batterypack mit nmc Zellen

voltage_lipo = battery_lipo.voltage(current) #Spannung in V von lipo
voltage_nmc = battery_nmc.voltage(current) #Spannung in V von nmc
logging.info("Setup: %s(%sWh), %s(%sWh)", lipo, round(battery_lipo.C_nom_Ah * battery_lipo.voltage(0)), nmc, round(battery_nmc.C_nom_Ah * battery_nmc.voltage(0))) #Loggt die Ausgangsleistung der beiden Akkus mit

power_el_lipo = motor.calc_power_el(voltage_lipo, current) #Elektrisches Leistungsprofil von lipo Batterypack
power_el_nmc = motor.calc_power_el(voltage_nmc, current) #Elektrisches Leistungsprofil von nmc Batterypack

plots.height_profile(timedt, elevation) #Höhenprofil alleine
plots.velocity_height_profile(timedt, elevation, velocity_kmh)  #Geschwindigkeits und Höhenverlauf übereinander

plots.height_power_profile(timedt, elevation, power_el_lipo, lipo) #Leistungs -und Höhenverlauf eines Lipoakkus plotten
plots.height_power_profile(timedt, elevation, power_el_nmc, nmc) #Leistungs -und Höhenverlauf eines Nmcakkus plotten

soc_verlauf_lipo = battery_lipo.simulate(time, current, lipo, timedt) #soc Verlauf Lipoakku bestimmen
plots.soc_profile(timedt, elevation, soc_verlauf_lipo, lipo) #Lade -und Höhenverlauf eines Lipoakkus plotten

soc_verlauf_nmc = battery_nmc.simulate(time, current, nmc, timedt) #soc Verlauf Nmcakku bestimmen
plots.soc_profile(timedt, elevation, soc_verlauf_nmc, nmc) #Lade -und Höhenverlauf eines Nmcakkus plotten

#Studie Radradius aus study.py
study.wheel_study(data_dict, 13.5, 17, lipo)    #13.5 = standard radius und 17 = beliebiger Radius für Studie

#unübersichtilicher Plot, habe dir Himmelsrichtung bei height_map hinzugefügt, wenn 
# man mit der Maus drüber fährt dieht man sie
#plots.compass_direction_plot(data_dict, compass_direction)

plot_height_map.height_map(data_dict, compass_direction)   #Die Höhenkarte über die Fahrt

h, m = gpsdata.calculate_total_time() #Berechnet Stunden und Minuten der Gesamtfahrtzeit 
logging.info("Gesamtfahrzeit: %sh%smin", h, m) #Logging für Gesamtzeit

totaldis = gpsdata.calculate_total_dis() #Berechnet die totale Distanz
logging.info("Zurueckgelegte Strecke: %skm", totaldis) #Logging für Gesamtstrecke

logging.info("Restakku: %s(%s%%), %s(%s%%)", lipo, round(soc_verlauf_lipo[-1], 2), nmc, round(soc_verlauf_nmc[-1], 2)) #Logging für Restakku

vm = gpsdata.calculate_vm() #Berechnet die mittlere Geschwindigkeit
logging.info("Mittlere Geschwindigkeit: %sm/s", vm) #Logging für mittlere Geschwindigkeit
             
asc, des = gpsdata.calculate_asc_des() #Berechnet den Anstieg und Abstieg 
logging.info("Hoehenmeter: Aufstieg(%sm), Abstieg:(%sm)", asc, des) #Logging für Höhenmeter Anstieg und Abstieg

maxpow = gpsdata.calculate_maxpow(power_mech) #Berechnet die maximale mechanische Leistung. Es wird nur 99% angeschaut die 1% der Spitzen werden dabei vernachlässigt.
logging.info("Maximale Leistung: %sW", maxpow) #Logging für maximale Leistung








