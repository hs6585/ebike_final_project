import numpy as np

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
        self.totaldis = 0
        self.sec = 0
        self.himmelsrichtung = 0

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

    def calculate_air_density(self):
        """Berechnet die Luftdichte"""
        
        # Luftdichte auf Meereshöhe
        rho_0 = 1.225  
        
        # Barometrische Höhenformel für die Troposphäre
        self.rho = rho_0 * (1 - 2.25577e-5 * self.ele) ** 4.25588
        
        return self.rho
    
    def calculate_drag_force(self, rho=1.2, cw_A=0.5625): #cw_A aus Aufgabenstellung entnommen
        """Berechnet die Luftwiderstandskraft."""
        self.F_D = 0.5 * rho * cw_A * (self.v ** 2)

        return self.F_D  
    
    def calculate_driving_force(self, m=80.0, g=9.81): #Masse = 10kg Rad + 70kg Fahrer
        """Berechnet die Antriebskraft"""

        F_H = m * g * np.sin(np.radians(self.incline_angle))
        F_acceleration = m * self.a
        
        self.F_A = F_acceleration + self.F_D + F_H
        return self.F_A 
    
    def calculate_vm(self):
        """Berechnet die Durchschnitttsgeschwindigkeit"""
        total_hours =  self.sec / 3600
        return round(self.totaldis / total_hours, 2)
    
    def calculate_asc_des(self):
        """Berechnet die Höhenmeter vom Aufstieg und Abstieg"""
        delta_ele = np.diff(self.ele)
        asc = np.sum(delta_ele[delta_ele > 0])
        des = np.sum(delta_ele[delta_ele < 0]) * -1
        return round(asc), round(des)
    
    def calculate_maxpow(self, power):
        """Berechnet die Maximalleistung"""
        real_max_power = np.percentile(power, 99) #Es wird das 99. Perzentil genommen, das ignoriert die obersten 1% der Messspitzen
        return round(float(real_max_power), 2)
    
    def calculate_total_dis(self):
        """Berechnet die zurückgelegte Strecke im 3D Raum"""
        s_sliced = self.s[1:]
        delta_ele = np.diff(self.ele)
        segments_3d = np.sqrt(s_sliced**2 + delta_ele**2) #Pythagoras anwenden
        total_3d_dis = np.sum(segments_3d)  #Aufsummieren und in Kilometer umrechnen
        self.totaldis = round(float(total_3d_dis) / 1000, 2)
        return self.totaldis
    
    def calculate_total_time(self):
        """Berechnet die gesamte benötigte Zeit"""
        self.sec = self.time[-1] - self.time[0] #Gesamtzeit berechnen
        h = int(self.sec / 3600)
        m = round((self.sec % 3600) // 60)
        return (h, m)

    def calculate_compass_direction(self):
        """Berechnet die Himmelsrichtungen"""
        
        delta_lon = np.diff(self.lon)   #Längengrad Differenz
        
        #Formel für Peilung auf einer Kugel
        x = np.sin(delta_lon) * np.cos(self.lat[1:])
        y = np.cos(self.lat[:-1]) * np.sin(self.lat[1:]) - (np.sin(self.lat[:-1]) * np.cos(self.lat[1:]) * np.cos(delta_lon))
        
        
        radiants = np.arctan2(x, y)  #schauen in welchem Quadrant
        grad = (np.degrees(radiants) + 360) % 360   #in Grad umwandeln und schauen dass es positiv ist
        
        richtungen = np.array(["N", "NO", "O", "SO", "S", "SW", "W", "NW"]) #alle Himmelsrichtungen
        
        # schauen dass der Bereich schön um z.b. Norden liegt und dann die richtige aus der Liste rausnehmen
        indices = ((grad + 22.5) / 45).astype(int) % 8
        himmelsrichtungen = richtungen[indices]
        
        #erste berechnete Himmelsrichtung als erste Stelle festlegen, damit dnach die Länge stimmt
        self.himmelsrichtung = np.insert(himmelsrichtungen, 0, himmelsrichtungen[0])
        
        return self.himmelsrichtung
    
        
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

    h = x.calculate_compass_direction()
    print(h[0])
    


        