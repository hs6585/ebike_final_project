import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from motor import Motor
from lipo_battery import LiPoBatteryPack
import calc_data_from_gps as gps
from calc_data_from_gps import CalcDataFromGPS
from readGPSdata import load_and_process_data




def wheel_study(data_dict, radius_standard, radius_groß, Akkutype:str):

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

    #Batterie:
    akku_small = LiPoBatteryPack(capacity_nom_Ah=30.0)
    akku_big = LiPoBatteryPack(capacity_nom_Ah=30.0)


    soc_verlauf_small = []
    soc_verlauf_big = []

    
    force = gps_data.calculate_driving_force()  #Antriebskraft

    time = gps_data.data_dict['time']
    time_dt = gps_data.data_dict['timedt']

    #Verlauf mit kleinem Rad
    torque_small = motor_small.calc_torque(force)
    current_small = motor_small.calc_current_motor(torque_small)
    simulation_small = akku_small.simulate(time, current_small, Akkutype, time_dt)
    soc_verlauf_small.append(simulation_small)

    #Verlauf mit großem Rad
    torque_big = motor_big.calc_torque(force)
    current_big = motor_big.calc_current_motor(torque_big)
    simulation_big = akku_big.simulate(time, current_big, Akkutype, time_dt)
    soc_verlauf_big.append(simulation_big)


    #Plotten:
    plt.figure(figsize=(10, 6))

    plt.plot(time_dt, soc_verlauf_small[0], color = "k", label = "Standard Radradius")
    plt.plot(time_dt, soc_verlauf_big[0], color = "r", label = "großer Radradius")


    # X-Achse in Uhrzeit formatiern
    x_axis = plt.gca()
    x_axis.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.title("SoC-Verlauf bei unterschiedlichen Radradien")
    plt.xlabel("Uhrzeit")
    plt.ylabel("SoC in %")
    plt.legend()

    plt.tight_layout()
    plt.show()

      

if __name__ == "__main__":

    lipo = "Lipo-Batterypack"
    nmc = "Nmc-Batterypack"

    data = "final_project_input_data.csv"
    data_dict = load_and_process_data(data)
    wheel_study(data_dict, 13.5, 17, nmc)
