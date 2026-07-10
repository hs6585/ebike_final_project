import geopandas as gpd
from shapely.geometry import LineString
from readGPSdata import load_and_process_data   #Funktion aus readGPSdata.py, sie gibt ein dict mit allen werten zurück
import matplotlib.pyplot as plt

def height_map(data_dict, compass_direction):   

    lat_list = data_dict['lat']
    lon_list = data_dict['lon']
    ele_list = data_dict['ele']
    temp_list = data_dict['temp']

    segments = []
    segment_elevations = []
    segment_directions = []

    for i in range(len(lat_list) - 1):  #pro Segment
        punkt1 = (lon_list[i], lat_list[i])
        punkt2 = (lon_list[i+1], lat_list[i+1])
        segments.append(LineString([punkt1, punkt2]))   #Segemente in Liste hinzufügen
        
        avg_ele = (ele_list[i] + ele_list[i+1]) / 2
        segment_elevations.append(avg_ele)  #damit man die mittlere Höhe hat, weil ein Segment hat immer nur eine Farbe
        segment_directions.append(compass_direction[i])

    data = {'geometry': segments, 'Hoehe': segment_elevations, 'Himmelsrichtung': segment_directions}
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    #Plot
    #gdf.plot(column='Hoehe', cmap='plasma', linewidth=3)
    #plt.show()
    #es ergibt wenig Sinn es als Plot zu machen weil man sich nichts drunter vorstellen kann

    #Karte wird als Datei gespeichert
    karte = gdf.explore(column='Hoehe', cmap='plasma', legend=True, legend_kwds=dict(colorbar=True), tooltip = ['Hoehe', 'Himmelsrichtung'])
    karte_fertig = "height_map.html"
    karte.save(karte_fertig)

    print("Höhenkarte wurde im Ornder gespeichert")
