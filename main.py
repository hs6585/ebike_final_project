import readGPSdata as gps
from calc_data_from_gps import CalcDataFromGPS
from motor import Motor
from lipo_battery import LiPoBatteryPack
from nmc_battery import NMCBatteryPack
import plots


csv_file = "final_project_input_data.csv" #CSV-Datei mit GPS-Messdatensatz
data_dict = gps.load_and_process_data(csv_file) #Dictionary mit GPS-Daten als float

gpsdata = CalcDataFromGPS(data_dict) #Initialisierung der Klasse CalcDataFromGPS
distance = gpsdata.calculate_distance() #Strecke in m       
velocity = gpsdata.calculate_speed() #Geschwindigkeit in m/s
accelearation = gpsdata.calculate_acceleration() #Beschleunigung in m/s^2
incline_angle = gpsdata.calculate_incline_angle() #Steigungswinkel in °
drag_force = gpsdata.calculate_drag_force() #Luftwiderstandskraft in N       
driving_force = gpsdata.calculate_driving_force() #Antriebskraft in N


elevation = gpsdata.data_dict["ele"] 
time = gpsdata.data_dict["time"]  
timedt = gpsdata.data_dict["timedt"]  
temp = gpsdata.data_dict["temp"]


#Motor
motor = Motor() #Initialisierung der Klasse Motor
power_mech = motor.calc_power_mech(driving_force, velocity) #Mechanisches Leistungsprofil in W
torque = motor.calc_torque(driving_force) #Drehmoment in Nm
current = motor.calc_current_motor(torque) #Motorstrom in A

#Batterie:
battery_lipo = LiPoBatteryPack(capacity_nom_Ah=30) #Batterypack mit lipo Zellen 
battery_nmc = NMCBatteryPack(capacity_nom_Ah=35) #Batterypack mit nmc Zellen


voltage_lipo = battery_lipo.voltage(current) #Spannung in V von lipo
voltage_nmc = battery_nmc.voltage(current) #Spannung in V von nmc
power_el_lipo = motor.calc_power_el(voltage_lipo, current) #Elektrisches Leistungsprofil von lipo Batterypack
power_el_nmc = motor.calc_power_el(voltage_nmc, current) #Elektrisches Leistungsprofil von nmc Batterypack

lipo = "Lipo-Batterypack"
nmc = "Nmc-Batterypack"

plots.height_power_profile(timedt, elevation, power_el_lipo, lipo) #Leistungs -und Höhenverlauf eines Lipoakkus plotten
plots.height_power_profile(timedt, elevation, power_el_nmc, nmc) #Leistungs -und Höhenverlauf eines Nmcakkus plotten

soc_verlauf_lipo = battery_lipo.simulate(time, current, lipo, timedt) #soc Verlauf Lipoakku bestimmen
plots.soc_profile(timedt, elevation, soc_verlauf_lipo, lipo) #Lade -und Höhenverlauf eines Lipoakkus plotten

soc_verlauf_nmc = battery_nmc.simulate(time, current, nmc, timedt) #soc Verlauf Nmcakku bestimmen
plots.soc_profile(timedt, elevation, soc_verlauf_nmc, nmc) #Lade -und Höhenverlauf eines Nmcakkus plotten







