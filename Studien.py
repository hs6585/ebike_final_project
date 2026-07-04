import readGPSdata as gps
from calc_data_from_gps import CalcDataFromGPS
from readGPSdata import load_and_process_data
from lipo_battery import LiPoBatteryPack
from motor import Motor

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import main as main


#ich will den wirkungsgrad in abh mit der zeit plotten. iwie ergibt es aber keinnen sinn.
# nochmal drüber schauen und vl umändern, damites eine sinnvolle studie ist

def temp_Studie(data_dict):
    

    csv_file = "final_project_input_data.csv" #CSV-Datei mit GPS-Messdatensatz
    data_dict = gps.load_and_process_data(csv_file) #Dictionary mit GPS-Daten als float

    time = main.time

    current = main.current
    p_mech = main.power_mech
    p_el = main.power_el_lipo
    p_loss = p_el - p_mech

    wirkungsgrad = p_mech / p_el
    resistance = p_loss / current**2


    #relativ sicher ergeben meine berechnungen keinen sinn
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(time, wirkungsgrad, color="k", linewidth=1.5)
    ax1.set_ylabel("Wirkungsgrad", fontsize=11)
    ax1.title.set_text("Zeit")
    ax1.grid(True, alpha=0.5)   #macht das gitter ein wenig transparent


    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    
    #Weil main auch eine datei ist werden alle plots dargestellt
    data = "final_project_input_data.csv"
    data_dictionary = load_and_process_data(data)
    temp_Studie(data_dictionary)
    print("Es klappt")