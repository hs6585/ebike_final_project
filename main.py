import readGPSdata as gps
from calc_data_from_gps import CalcDataFromGPS
from motor import Motor
from lipo_battery import LiFePO4BatteryPack
from nmc_battery import NMCBatteryPack

import matplotlib.pyplot as plt
import numpy as np


csv_file = "final_project_input_data.csv"
data_dict = gps.load_and_process_data(csv_file) 

gpsdata = CalcDataFromGPS(data_dict) 
distance = gpsdata.calculate_distance()           
velocity = gpsdata.calculate_speed()              
accelearation = gpsdata.calculate_acceleration()   
incline_angle = gpsdata.calculate_incline_angle() 
drag_force = gpsdata.calculate_drag_force()        
driving_force = gpsdata.calculate_driving_force() 


elevation = gpsdata.data_dict["ele"]
time = gpsdata.data_dict["time"]    
temp = gpsdata.data_dict["temp"]


# Motor
motor = Motor() 
power_mech = motor.calc_power_mech(driving_force, velocity) 
torque = motor.calc_torque(driving_force) 
current = motor.calc_current_motor(torque) 

#Batterie:
battery_lipo = LiFePO4BatteryPack(capacity_nom_Ah=30) 
battery_nmc = NMCBatteryPack(capacity_nom_Ah=30)


voltage_lipo = battery_lipo.voltage(current) 
voltage_nmc = battery_nmc.voltage(current) 
power_el_lipo = motor.calc_power_el(voltage_lipo, current)
power_el_nmc = motor.calc_power_el(voltage_nmc, current) 



#Höhenverlauf und Leistungsverlauf plotten:

x_axis = time 
height = elevation  
power = power_el_lipo 

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)


ax1.plot(x_axis, power, color="k", linewidth=1.5, label="elektrische Leistung")
ax1.set_ylabel("Leistung [W]", fontsize=11)
ax1.title.set_text("Höhen- und Leistungsverlauf über die Zeit")
ax1.grid(True, alpha=0.5)   #macht das gitter ein wenig transparent weil sonst störts

ax2.plot(x_axis, height, color = "r", linewidth=2, label="Höhe")
ax2.set_xlabel("Zeit [s]", fontsize=11)
ax2.set_ylabel("Höhe [m]", fontsize=11)
ax2.grid(True, alpha=0.5)

plt.tight_layout()
plt.show()

#------------------------------------------
#Ladeverlauf und Höhenverlauf plotten:

height = elevation  

for i in range(1, len(time)):
    delta_t = time[i] - time[i-1]
    strom_aktuell = current[i]

    battery_lipo.apply_current(strom_aktuell, delta_t)

soc_verlauf = battery_lipo.get_history()
soc_verlauf.insert(0, 1.0)  #damit die länge der liste weiterhin richtig bleibt


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

ax1.plot(time, soc_verlauf, color="k", linewidth=1.5, label="Ladezustand")
ax1.set_ylabel("Ladezustand (%)", fontsize=11)
ax1.title.set_text("Ladezustand der Batterie")
ax1.grid(True, alpha=0.5)   #macht das gitter ein wenig transparent weil sonst störts

ax2.plot(time, height, color = "r", linewidth=2, label="Höhe")
ax2.set_xlabel("Zeit [s]", fontsize=11)
ax2.set_ylabel("Höhe [m]", fontsize=11)
ax2.grid(True, alpha=0.5)

plt.tight_layout()
plt.show()
