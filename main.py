import readGPSdata as gps
from calc_data_from_gps import CalcDataFromGPS
from motor import Motor
from lipo_battery import LiFePO4BatteryPack

#Csv Datei mit der GPS-Messdatenreihe
csv_file = "final_project_input_data.csv"

#Messdaten als float in Dictionary speichern
data_dict = gps.load_and_process_data(csv_file) 

gpsdata = CalcDataFromGPS(data_dict) #Dictionary an GPS-Verarbeitungsklasse übergeben und Klasse initialisieren
distance = gpsdata.calculate_distance() #Strecke in m berechnen
velocity = gpsdata.calculate_speed() #Geschwindigkeit in m/s berechnen
accelearation = gpsdata.calculate_acceleration() #Beschleunigung in m/s^2 berechnen
incline_angle = gpsdata.calculate_incline_angle() #Steigungswinkel in ° berechnen
drag_force = gpsdata.calculate_drag_force() #Luftwiderstandskraft in N berechnen
driving_force = gpsdata.calculate_driving_force() #Antriebskraft in N berechnen

motor = Motor() #Klasse Motor initialisieren
power_mech = motor.calc_power_mech(driving_force, velocity[:-1]) #Mechanische Leistung in W berechnen
torque = motor.calc_torque(driving_force) #Drehmoment in Nm berechnen
current = motor.calc_current_motor(torque) #Motorstrom in A berechnen

battery = LiFePO4BatteryPack(capacity_nom_Ah=100) #Kapazität übergeben und Klasse Batterypack initialisieren
voltage = battery.voltage(current) #Spannung in V berechnen
power_el = motor.calc_power_el(voltage, current) #Elektrische Leistung in W berechnen

#Prints vorläufig nur zum testen
print(f"Leistungsprofil mech: {power_mech[:4]}")
print(f"Leistungsprofil ele: {power_el[:4]}")
print(f"Antriebskraft: {driving_force[:4]}")
print(f"Drehmoment: {torque[:4]}")
print(f"Beschleunigung: {accelearation[:4]}")
print(f"Geschwindigkeit: {velocity[:4]}")
print(f"Strecke: {distance[:4]}")
print(f"Strom:{current[:4]}")

