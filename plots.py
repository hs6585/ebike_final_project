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
    
def plot_voltage_and_current_profile(voltage_profile: list[float], current_profile: list[float], duration_profile: list[float], akkutype: str):
    
    """Plots the voltage and current over time profiles starting from t=0s. 
    The voltage_profile must start with the initial voltage at t=0s, and the subsequent voltage values correspond to the voltage after applying the current for the respective duration intervals.
    The voltage and current are assumed to be piecewise constant over the given duration intervals.

    Parameters
    ----------
    voltage_profile : list[float]
        List of voltage values in Volts (V) for each interval. Plus the initial voltage at t=0s.
    current_profile : list[float]
        List of current values in Amperes (A) for each interval.
    duration_profile : list[float]
        List of duration values in seconds (s) for each interval. Must have the same length as voltage_profile and current_profile.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The matplotlib figure object containing the plot of voltage and current over time."""


    assert len(voltage_profile) - 1 == len(current_profile) == len(duration_profile), "Current and duration profiles must have the same length, and voltage profile must be longer by 1 to account for the starting voltage at t=0s."

    t_plot, U_plot, I_plot = [], [], []

    t_plot.append(0.0)
    U_plot.append(voltage_profile[0])

    t_total = 0.0
    for U, I, d in zip(voltage_profile[1:], current_profile, duration_profile):
        t_plot += [t_total, t_total + d]
        U_plot += [U, U]
        I_plot += [I, I]

        t_total += d

    fig, axV = plt.subplots(figsize=(9, 4.5))
    axI = axV.twinx()

    axI.title.set_text(f"Spannungs- und Stromverlauf {akkutype}")
    axV.plot(t_plot[0:], U_plot, "b-", label="Voltage U / V")
    axI.plot(t_plot[1:], I_plot, "r--", label="Current I / A")
    axV.set_xlabel("Time $t$ / s")
    axV.set_ylabel("Voltage $U$ / V", color="b")
    axI.set_ylabel("Current $I$ / A", color="r")
    axV.grid(True)
    
    fig.legend(loc="upper right", bbox_to_anchor=(0.85, 0.85))


def plot_air_density(time_dt, height, rho):

    #Die Luftdichte ist in diesem Fall nicht exponentiell erkennbar, weil es bei so geringen Höhenunterschieden minimal ist.

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(time_dt, rho, color="k", linewidth=1.5, label="Luftdichte")
    ax1.set_ylabel("Luftdichte", fontsize=11)
    ax1.title.set_text(f"Luftdichte in Abhängigkeit der Höhe")
    ax1.grid(True, alpha=0.5)   #macht das gitter ein wenig transparent

    ax2.plot(time_dt, height, color = "r", linewidth=2, label="Höhe")
    ax2.set_xlabel("Uhrzeit", fontsize=11)
    ax2.set_ylabel("Höhe [m]", fontsize=11)
    ax2.grid(True, alpha=0.5)

    # X-Achse in Stunde:Minute formatiern
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.tight_layout()

