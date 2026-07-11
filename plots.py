import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import geopandas as gpd
from shapely.geometry import LineString

def height_profile(time_dt, height):

    plt.figure(figsize=(10, 6))

    plt.plot(time_dt, height, color = "k")


    # X-Achse in Uhrzeit formatiern
    x_axis = plt.gca()
    x_axis.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.title("Höhenprofil")
    plt.xlabel("Uhrzeit")
    plt.ylabel("Höhe in Meter")

    plt.tight_layout()
    

def velocity_height_profile(time_dt, height, velocity):

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), sharex=True)

    ax1.plot(time_dt, velocity, color="k", linewidth=1.5, label="Geschwindigkeit")
    ax1.set_ylabel("Geschwindigkeit in km/h", fontsize=11)
    ax1.title.set_text(f"Geschwindigkeitsverlauf")
    ax1.grid(True, alpha=0.5)   #macht das gitter ein wenig transparent

    ax2.plot(time_dt, height, color = "r", linewidth=2, label="Höhe")
    ax2.set_xlabel("Uhrzeit", fontsize=11)
    ax2.set_ylabel("Höhe [m]", fontsize=11)
    ax2.grid(True, alpha=0.5)

    # X-Achse in Stunde:Minute formatiern
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.tight_layout()
    

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
    


