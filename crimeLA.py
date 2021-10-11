import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import Marker
from folium.plugins import MarkerCluster


data = pd.read_csv(r'Crime_Data_from_2010_to_2019.csv')
data = data[(data['LAT']!= 0) & (data['LON'] !=0)]
data = data.drop(columns=['DATE OCC', 'TIME OCC', 'AREA ', 'Part 1-2', 'Crm Cd Desc', 'Mocodes', 'Premis Cd', 'Premis Desc', 'Weapon Used Cd', 'Weapon Desc', 'Status', 'Status Desc', 'Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4', 'Cross Street'])
data['Date Rptd'] = pd.to_datetime(data['Date Rptd'], errors='coerce')
data['year']= data['Date Rptd'].dt.year

# Get the latest date (we loop years later)
freshDate = max(data.year)

# Get the crime data of the year 
crimeByYear = data.loc[(data.year == freshDate)]

# Create the map
my_map = folium.Map(location=[34.052235,-118.243683], tiles='OpenStreetMap', zoom_start=4)

# Add points to the map
mc = MarkerCluster()

for idx, row in crimeByYear.iterrows(): 

    if not math.isnan(row['LON']) and not math.isnan(row['LAT']):
    
        # Create pop-up message for each point 
        pop = ["Vict Age", "Vict Sex", "Vict Descent"]
        popmsg = [str(item) + ':' + str(row[item]) for item in pop]
        popmsg = '\n'.join(popmsg)
        # Add marker to mc
        mc.add_child(Marker(location=[row['LAT'], row['LON']],  popup=popmsg, tooltip=str(row['LOCATION'])))

# Add mc to map
my_map.add_child(mc)

# Save the map
my_map.save('map_1.html')
