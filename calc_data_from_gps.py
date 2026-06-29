import numpy as np

def calculate_distance(data_dict):
    """
    Berechnet die Teilstrecken zwischen den GPS-Punkten.
    """
    R = 6371000  #Erdradius in Meter
    
    #Daten aus dem dict herausholen
    lat = data_dict["lat"]
    lon = data_dict["lon"]
    
    #Koordinaten von Grad in Rad umrechnen
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    
    #Slicen
    lat1 = lat_rad[:-1]
    lat2 = lat_rad[1:]
    lon1 = lon_rad[:-1]
    lon2 = lon_rad[1:]
    
    #Delta lat und lon berechnen
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    #Haversine Formel anwenden
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    delta_s = R * c
    
    return delta_s #in m

def calculate_speed(data_dict, delta_s):
    """
    Berechnet die Geschwindigkeit zwischen den GPS Punkten.
    """
    time = data_dict["time"]
    
    #deltaT berechnen
    delta_t = time[1:] - time[:-1]
    
    #Geschwindigkeit berechnen
    v = delta_s / delta_t
    
    return v #in m/s

def calculate_acceleration(data_dict, v):
    """
    Berechnet die Beschleunigung zwischen den GPS Punkten.
    """
    time = data_dict["time"]
    
    #deltaT berechnen
    delta_t = time[1:] - time[:-1]
    delta_t_acceleration = (delta_t[1:] + delta_t[:-1]) / 2
    
    #deltaV berechnen
    delta_v = v[1:] - v[:-1]

    #Beschleunigung berechnen
    a = delta_v / delta_t_acceleration
    
    return a #in m/s^2

if __name__ == "__main__":

    from readGPSdata import load_and_process_data
    data_dict = load_and_process_data("final_project_input_data.csv")

    s = calculate_distance(data_dict)
    print("Erste Teilstrecke in m:", s[0])

    v = calculate_speed(data_dict, s)
    print("Erste Teilgeschwindigkeit in m/s:", (v[0]))

    a = calculate_acceleration(data_dict, v)
    print("Erste Teilbeschleunigung in m/s^2:", (a[0]))