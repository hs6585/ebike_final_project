import readGPSdata as gps
from calc_data_from_gps import CalcDataFromGPS

#Csv datei mit der GPS-Messdatenreihe
csv_file = "final_project_input_data.csv"

#Messdaten als float in Dictionary speichern
data_dict = gps.load_and_process_data(csv_file) 

x = CalcDataFromGPS(data_dict)
distance = x.calculate_distance() #Strecke in m
velocity = x.calculate_speed() #Geschwindigkeit in m/s
accelearation = x.calculate_acceleration() #Beschleunigung in m/s^2
incline_angle = x.calculate_incline_angle() #Steigungswinkel in °
drag_force = x.calculate_drag_force() #Luftwiderstandskraft in N
driving_force = x.calculate_driving_force() #Antriebskraft in N


