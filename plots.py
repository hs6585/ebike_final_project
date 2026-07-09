import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import geopandas as gpd
from shapely.geometry import LineString

def height_power_profile(time_dt, height, power, Akkutype:str):

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(time_dt, power, color="k", linewidth=1.5, label="Elektrische Leistung")
    ax1.set_ylabel("Leistung [W]", fontsize=11)
    ax1.title.set_text(f"Leistungs -und Höhenverlauf über die Zeit mit einem {Akkutype}")
    ax1.grid(True, alpha=0.5)   #macht das gitter ein wenig transparent

    ax2.plot(time_dt, height, color = "r", linewidth=2, label="Höhe")
    ax2.set_xlabel("Uhrzeit", fontsize=11)
    ax2.set_ylabel("Höhe [m]", fontsize=11)
    ax2.grid(True, alpha=0.5)

    # X-Achse in Stunde:Minute formatiern
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.tight_layout()
    plt.show()

def soc_profile(time_dt, height, soc_verlauf, Akkutype:str):
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(time_dt, soc_verlauf, color="k", linewidth=1.5, label="Ladezustand")
    ax1.set_ylabel("Ladezustand [%]", fontsize=11)
    ax1.title.set_text(f"Ladezustand und Höhenverlauf mit einem {Akkutype}")
    ax1.grid(True, alpha=0.5)   #macht das gitter ein wenig transparent weil sonst störts

    ax2.plot(time_dt, height, color = "r", linewidth=2, label="Höhe")
    ax2.set_xlabel("Uhrzeit", fontsize=11)
    ax2.set_ylabel("Höhe [m]", fontsize=11)
    ax2.grid(True, alpha=0.5)

    # X-Achse in Stunde:Minute formatiern
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.tight_layout()
    plt.show()

def compass_direction_plot(data_dict, compass_direction):

    lat_list = data_dict['lat']
    lon_list = data_dict['lon']

    segments = []
    segment_directions = []

    # danach für Farbe
    mapping = {"N": 0, "NO": 1, "O": 2, "SO": 3, "S": 4, "SW": 5, "W": 6, "NW": 7}

    for i in range(len(lat_list) - 1):  # pro Segment
        punkt1 = (lon_list[i], lat_list[i])
        punkt2 = (lon_list[i+1], lat_list[i+1])
        segments.append(LineString([punkt1, punkt2]))   # Segmente in Liste hinzufügen
        
        # Richtung des aktuellen Punktes holen und als Zahl speichern und mit Liste vergleichen
        richtung_text = compass_direction[i]
        richtung_zahl = mapping.get(richtung_text, 0)
        segment_directions.append(richtung_zahl)
        
    #wie in plot_height_map
    data = {'geometry': segments, 'Richtung': segment_directions}
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    gdf.plot(column='Richtung', cmap='hsv', linewidth=3, legend = True)

    plt.title("Legende: 0=N | 1=NO | 2=O | 3=SO | 4=S | 5=SW | 6=W | 7=NW", fontsize=10)

    plt.show()



