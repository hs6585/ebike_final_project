import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
