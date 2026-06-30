import numpy as np

class CalcDataFromGPS():

    def __init__(self, data_dict: dict):
        self.data_dict = data_dict
        self.delta_s = []
        self.v = []
        self.a = []
        self.incline_angle = []

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
    
    def calculate_incline_angle(self):
        """
        Berechnet die Steigung zwischen den GPS Punkten.
        """
        ele = self.data_dict["ele"]
        
        #deltaH berechnen
        delta_h = ele[1:] - ele[:-1]

        #Steigungswinkel in RAD berechnen
        angle_rad = np.arctan2(delta_h, self.delta_s)

        # Bogenmaß in Grad umrechnen für bessere Lesbarkeit
        self.incline_angle = np.degrees(angle_rad)
        
        return self.incline_angle #in Grad

        
if __name__ == "__main__":

    data_dict = data_dict = {
    "lat": np.array([47.583114, 47.582910, 47.582820]),
    "lon": np.array([12.170826, 12.170766, 12.170733]),
    "ele": np.array([494.888597, 494.888597, 494.888597]),
    "time": np.array([14.187, 16.665, 17.800]),
    "temperature": np.array([28.69968, 28.85415, 28.69915])}
    
    x = CalcDataFromGPS(data_dict)
    s = x.calculate_distance()
    print("Erste Teilstrecke in m:", s[0])
    v = x.calculate_speed()
    print("Erste Teilgeschwindigkeit in m/s:", (v[0]))
    a = x.calculate_acceleration()
    print("Erste Teilbeschleunigung in m/s^2:", (a[0]))
    p = x.calculate_incline_angle()
    print("Erster Steigungswinkel in °:", (p[0]))

        