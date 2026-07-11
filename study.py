import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import logging

from motor import Motor
from lipo_battery import LiPoBatteryPack  # Wird für die Batterie-Instanziierung benötigt
import calc_data_from_gps as gps
from calc_data_from_gps import CalcDataFromGPS
from readGPSdata import load_and_process_data
from ebike_simulator import EBikeSimluator



def wheel_study(data_dict, radius_standard, radius_groß):

    lipo_small = "Lipo-Batterypack mit kleinem Radradius"
    lipo_big = "Lipo-Batterypack mit grossem Radradius"

    #Berechnungen werden durchgeführt, damit force nicht None ist
    gps_data = CalcDataFromGPS(data_dict)
    gps_data.calculate_distance()         
    gps_data.calculate_speed()            
    gps_data.calculate_acceleration()     
    gps_data.calculate_incline_angle()    
    gps_data.calculate_drag_force()       

    #Motor:
    motor_small = Motor(1.5, radius_standard)
    motor_big = Motor(1.5, radius_groß)

    #Batterie-Objekte erstellen, da der EBikeSimluator diese zwingend im Konstruktor erwartet
    battery_small = LiPoBatteryPack(capacity_nom_Ah=30, cells_in_parallel=1)
    battery_big = LiPoBatteryPack(capacity_nom_Ah=30, cells_in_parallel=1)
    logging.info("Setup Simulation fuer Studie(Radradius): %s(%sWh), %s(%sWh)", lipo_small, round(battery_small.C_nom_Ah * battery_small.voltage(0)), lipo_big, round(battery_big.C_nom_Ah * battery_big.voltage(0))) #Loggt die Ausgangsleistung der beiden Akkus mit

    #Simulatoren korrekt initialisieren (mit Batterie und Motor)
    akku_small = EBikeSimluator(battery_small, motor_small)
    akku_big = EBikeSimluator(battery_big, motor_big)

    force = gps_data.calculate_driving_force()  #Antriebskraft

    time = gps_data.data_dict['time']
    time_dt = gps_data.data_dict['timedt']

    # Delta-Zeitprofil berechnen (wie in main.py benötigt für das Lastprofil)
    duration_profile = np.diff(time)

    #Verlauf mit kleinem Rad simulieren
    torque_small = motor_small.calc_torque(force)
    # Da duration_profile um 1 kürzer ist als time, übergeben wir time_dt[:-1] für das Logging
    akku_small.simulate(torque_small, duration_profile, time_dt[:-1], lipo_small)
    soc_verlauf_small = akku_small.soc_profile

    #Verlauf mit großem Rad simulieren
    torque_big = motor_big.calc_torque(force)
    akku_big.simulate(torque_big, duration_profile, time_dt[:-1], lipo_big)
    soc_verlauf_big = akku_big.soc_profile

    #Plotten:
    plt.figure(figsize=(10, 6))

    # Die x-Achse wird ebenfalls auf time_dt[:-1] angepasst, da das SoC-Profil der simulierten Schritte entspricht
    plt.plot(time_dt, soc_verlauf_small, color = "k", label = "Standard Radradius")
    plt.plot(time_dt, soc_verlauf_big, color = "r", label = "Großer Radradius")


    # X-Achse in Uhrzeit formatiern
    x_axis = plt.gca()
    x_axis.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.title("SoC-Verlauf bei unterschiedlichen Radradien")
    plt.xlabel("Uhrzeit")
    plt.ylabel("SoC in %")
    plt.legend()

    plt.tight_layout()
    lipo = "Lipo-Batterypack"
    logging.info("Restakku: %s(%s%%), %s(%s%%)", lipo_small, round(battery_small.soc*100, 2), lipo_big, round(battery_big.soc*100, 2)) #Logging für Restakku
      

if __name__ == "__main__":

    lipo = "Lipo-Batterypack"
    nmc = "Nmc-Batterypack"

    data = "final_project_input_data.csv"
    data_dict = load_and_process_data(data)
    wheel_study(data_dict, 13.5, 17)
