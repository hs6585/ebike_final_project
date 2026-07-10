class Motor:

    def __init__(self, motorconstant_Nm_A: float = 1.5, wheel_radius_inch: float = 13.5):
        self.c_m = motorconstant_Nm_A
        self.wheel_r = wheel_radius_inch / 39.37 #Radius in Meter

    def calc_power_mech(self, force_N: float, velocity_m_s: float) -> float: #mechanische Leistung F*v berechnen
        mech_power = force_N * velocity_m_s
        return mech_power
    
    def calc_power_el(self, voltage_V: float, current_A:float) -> float:    #elektrsche Leistung U*I
        el_power = voltage_V * current_A
        return el_power

    def calc_power_el(self, voltage_V: float, current_A: float):
        el_power = [v * i for v, i in zip(voltage_V, current_A)]
        return el_power

    def calc_torque(self, force_N: float) -> float:     #Drehmoment mit F*r berechnen
        torque = force_N * self.wheel_r
        return torque

    def calc_current_motor(self, torque_Nm: float) -> float:    #Motorstrom mit Drehmoment/Konstante
        current_motor = torque_Nm / self.c_m
        return current_motor 
    

if __name__ == "__main__":
    motor = Motor()
    print(f"Drehmoment bei F=100N: {motor.calc_torque(200)} Nm")
    drehmoment = motor.calc_torque(200)
    print(f"Motorstrom bei 200Nm: {motor.calc_current_motor(drehmoment)} A")
    
    

    
