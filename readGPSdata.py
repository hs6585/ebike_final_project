import numpy as np

def load_and_process_data(file_path):
    """
    Lädt die CSV-Datei und gibt die verarbeiteten Daten als Dictionary zurück.
    """
    #Die gesamte CSV-Datei als Text-Matrix einlesen, Kopfzeile wird mit skiprows = 1 übersprungen 
    data = np.loadtxt(file_path, delimiter=";", skiprows=1, dtype=str) 

    #.astype konvertiert die str Spalten in eine float Spalte
    lat = data[:, 0].astype(float) 
    lon = data[:, 1].astype(float)
    ele = data[:, 2].astype(float)
    time_str = data[:, 3]
    temp = data[:, 4].astype(float)

    #Zeit in float mit numpy datetime umrechen
    time_dt = time_str.astype('datetime64[ms]') #In ms um alle Nachkommastellen zu berücksichtigen
    time = time_dt.astype(float) / 1000.0 #Durch 1000 Teilen um Zeit in Sekunden zu erhalten

    return { "lat": lat,"lon": lon,"ele": ele,"time": time,"temp": temp}

if __name__ == "__main__":
    file = "final_project_input_data.csv"
    data_dict = load_and_process_data(file)
    
    print("Erste Temperaturwerte:", data_dict["temp"][:5])
    