from abc import ABC, abstractmethod

"""In der csv Datei sind folgende Daten: x- und y-Koordinaten, 
aktuelle Höhe, aktuelle Zeit, aktuelle Temperatur"""


class BatteryBase(ABC):
    """
    Abstrakte Basisklasse für das Batteriesystem. Diese Datei ist die Basis für battery pack.
    """
    
    @abstractmethod
    def __init__(self, capacity_nom_Ah: float, initial_soc: float):
        """
        capacity_nom = Kapazität des Akkus
        initial_soc = state of charge (entlade, aufladen, bleiben)
        """
        pass

    @abstractmethod
    def apply_current(self, current: float, duration: float) -> None:
        """
        Hier wird der state of charge (soc) danach bestimmt.
        Dieser ist entweder kleiner oder größer als 0, der Akku wird also entladen oder geladen.
        (Die Formel wird aus den Vorlesungsunterlagen genommen)
        """
        pass

    @abstractmethod
    def voltage(self, current: float = 0.0) -> float:
        """
        Hier wird die Spannung U bestimmt
        (Die Formel wird aus den VO_Unterlagen genommen)
        """
        pass

    @abstractmethod
    def get_history(self) -> dict:
        
        #Hier wird der Verlauf der Batterie gespeichert, um danach die Daten plotten zu können
        
        pass


