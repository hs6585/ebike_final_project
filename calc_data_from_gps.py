import numpy as np

"""class CalcDataFromGPS():

    def __init__(self, data_dict: dict):
        self.data_dict = data_dict
        self.delta_s = []
        self.v = []
        self.a = []
        self.incline_angle = []
        self.F_D = []
        self.F_A = []

    def calculate_distance(self):
        
        #Berechnet die Teilstrecken zwischen den GPS-Punkten.
        
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
        
        #Berechnet die Geschwindigkeit zwischen den GPS Punkten.
        
        time = self.data_dict["time"]
        
        #deltaT berechnen
        delta_t = time[1:] - time[:-1]
        
        #Geschwindigkeit berechnen
        self.v = self.delta_s / delta_t
        
        return self.v #in m/s

    def calculate_acceleration(self):
        
        #Berechnet die Beschleunigung zwischen den GPS Punkten.
        
        time = self.data_dict["time"]
        
        #deltaT berechnen
        delta_t_acceleration = (delta_t[1:] + delta_t[:-1]) / 2    
        
        #deltaV berechnen
        delta_v = self.v[1:] - self.v[:-1] 

        #Beschleunigung berechnen
        self.a = delta_v / delta_t_acceleration 
        
        return self.a #in m/s^2
    
    def calculate_incline_angle(self):
        
        #Berechnet die Steigung zwischen den GPS Punkten.
        
        ele = self.data_dict["ele"]
        
        #deltaH berechnen
        delta_h = ele[1:] - ele[:-1]

        #Steigungswinkel in RAD berechnen
        angle_rad = np.arctan2(delta_h, self.delta_s)

        # Bogenmaß in Grad umrechnen für bessere Lesbarkeit
        self.incline_angle = np.degrees(angle_rad)
        
        return self.incline_angle #in Grad
    
    def calculate_drag_force(self, rho=1.2, cw_A=0.5625):
        "
        #Berechnet die Luftwiderstandskraft F_D zwischen den GPS Punkten.
        
        self.F_D = 0.5 * rho * cw_A * (self.v ** 2)
        return self.F_D # in N
    
    def calculate_driving_force(self, m=80.0, g=9.81):
        
        #Berechnet die notwendige Antriebskraft in Newton.
        
        #Array für Luftwiderstandskraft und Steigungswinkel um 1 kürzen, damit es gleichlang wie das Beschleunigungsarray ist
        F_D_aligned = self.F_D[:-1]
        angle_aligned = self.incline_angle[:-1]
        
        #Hangabtriebskraft berechnen
        F_H = m * g * np.sin(np.radians(angle_aligned))
        
        #Beschleunigungskraft berechnen
        F_acceleration = m * self.a
        
        #Antriebskraft berechnen
        self.F_A = F_acceleration + F_D_aligned + F_H
        
        return self.F_A #in Newton
        
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
    F_D = x.calculate_drag_force()
    print("Erste Luftwiderstandskraft in N:", (F_D[0]))
    F_A = x.calculate_driving_force()
    print("Erste Antriebskraft in N:", (F_A[0]))"""


    #------------------------------------------------------------------------









class CalcDataFromGPS():

    def __init__(self, data_dict: dict):
        self.data_dict = data_dict
        self.lat = np.radians(data_dict["lat"])
        self.lon = np.radians(data_dict["lon"])
        self.ele = data_dict["ele"]
        self.time = data_dict["time"]
        
        self.s = None
        self.v = None
        self.a = None
        self.incline_angle = None
        self.F_D = None
        self.F_A = None

    def calculate_distance(self):
        """Berechnet die Teilstrecken zwischen den GPS-Punkten."""
        R = 6371000  # Erdradius in Meter
        dlat = np.diff(self.lat)
        dlon = np.diff(self.lon)

        #Haversine Formel:
        a = np.sin(dlat / 2)**2 + np.cos(self.lat[:-1]) * np.cos(self.lat[1:]) * np.sin(dlon / 2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        
        # Um die Originallänge beizubehalten und danach kein Chaos mit den Längen der
        #Listen zu haben, fügt man eine 0 hinzu
        self.s = np.insert(R * c, 0, 0.0)

        return self.s 

    def calculate_speed(self):
        """Berechnet die Geschwindigkeit direkt auf den Zeitpunkten."""

        #die Funktion cumsum ist hier sehr raktisch, weil sie die Teilstrecken 
        #zwischen den Punkten in einen fortlaufenden Kilometerstand verwandelt.
        self.v = np.gradient(np.cumsum(self.s), self.time)

        return self.v 

    def calculate_acceleration(self):
        """Berechnet die Beschleunigung zeitsynchron zur Geschwindigkeit."""
        self.a = np.gradient(self.v, self.time)

        return self.a  
    
    def calculate_incline_angle(self):
        """Berechnet den Steigungswinkel direkt auf den Zeitpunkten."""

        delta_h = np.gradient(self.ele, self.time)
        
        angle_rad = np.arctan2(delta_h, self.v)
        self.incline_angle = np.degrees(angle_rad)

        return self.incline_angle  
    
    def calculate_drag_force(self, rho=1.2, cw_A=0.5625):
        """Berechnet die Luftwiderstandskraft."""
        self.F_D = 0.5 * rho * cw_A * (self.v ** 2)

        return self.F_D  
    
    def calculate_driving_force(self, m=80.0, g=9.81):
        """Berechnet die Antriebskraft"""

        F_H = m * g * np.sin(np.radians(self.incline_angle))
        F_acceleration = m * self.a
        
        self.F_A = F_acceleration + self.F_D + F_H
        return self.F_A 
        
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
    F_D = x.calculate_drag_force()
    print("Erste Luftwiderstandskraft in N:", (F_D[0]))
    F_A = x.calculate_driving_force()
    print("Erste Antriebskraft in N:", (F_A[0]))
    


        