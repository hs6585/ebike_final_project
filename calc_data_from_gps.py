import numpy as np

class CalcDataFromGPS():

    def __init__(self, data_dict: dict):
        self.data_dict = data_dict
        self.delta_s = []
        self.v = []
        self.a = []

    def calculate_distance(self):
        """
        Berechnet die Teilstrecken zwischen den GPS-Punkten.
        """
        R = 6371000  #Erdradius in Meter
        
        #Daten aus dem dict herausholen
        lat = self.data_dict["lat"]
        lon = self.data_dict["lon"]
        
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
        
        self.delta_s = R * c
        
        return self.delta_s #in m

    def calculate_speed(self):
        """
        Berechnet die Geschwindigkeit zwischen den GPS Punkten.
        """
        time = self.data_dict["time"]
        
        #deltaT berechnen
        delta_t = time[1:] - time[:-1]
        
        #Geschwindigkeit berechnen
        self.v = self.delta_s / delta_t
        
        return self.v #in m/s

    def calculate_acceleration(self):
        """
        Berechnet die Beschleunigung zwischen den GPS Punkten.
        """
        time = self.data_dict["time"]
        
        #deltaT berechnen
        delta_t = time[1:] - time[:-1]
        delta_t_acceleration = (delta_t[1:] + delta_t[:-1]) / 2
        
        #deltaV berechnen
        delta_v = self.v[1:] - self.v[:-1]

        #Beschleunigung berechnen
        self.a = delta_v / delta_t_acceleration
        
        return self.a #in m/s^2

if __name__ == "__main__":

    from readGPSdata import load_and_process_data
    data_dict = load_and_process_data("final_project_input_data.csv")
    
    x = CalcDataFromGPS(data_dict)
    
    s = x.calculate_distance()
    print("Erste Teilstrecke in m:", s[0])
    v = x.calculate_speed()
    print("Erste Teilgeschwindigkeit in m/s:", (v[0]))
    a = x.calculate_acceleration()
    print("Erste Teilbeschleunigung in m/s^2:", (a[0]))

        