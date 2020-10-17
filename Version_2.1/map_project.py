import pandas as pd # library for data analsysis
import json # library to handle JSON files
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
import requests # library to handle requests
import numpy as np
import folium # map rendering library
import streamlit as st
from streamlit_folium import folium_static
#------------------------------------------------

data_all = pd.read_csv('Surabaya_Full_of_Data.csv')
data_geo = json.load(open('Kecamatan_Surabaya.geojson'))

def center():
    address = 'Surabaya, ID'
    geolocator = Nominatim(user_agent="id_explorer")
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude
    return latitude, longitude

def threshold(data):
    threshold_scale = np.linspace(data_all[dicts[data]].min(),
                              data_all[dicts[data]].max(),
                              10, dtype=float)
    threshold_scale = threshold_scale.tolist() # change the numpy array to a list
    threshold_scale[-1] = threshold_scale[-1]
    return threshold_scale

def show_maps(data, threshold_scale):
    maps= folium.Choropleth(
        geo_data = data_geo,
        data = data_all,
        columns=['District',dicts[data]],
        key_on='feature.properties.name',
        threshold_scale=threshold_scale,
        fill_color='YlOrRd', 
        fill_opacity=0.7, 
        line_opacity=0.2,
        legend_name=dicts[data],
        highlight=True,
        reset=True).add_to(map_sby)

    folium.LayerControl().add_to(map_sby)
    maps.geojson.add_child(folium.features.GeoJsonTooltip(fields=['name',data],
                                                        aliases=['District: ', dicts[data]],
                                                        labels=True))                                                       
    folium_static(map_sby)

centers = center()

select_maps = st.sidebar.selectbox(
    "What data do you want to see?",
    ("OpenStreetMap", "Stamen Terrain","Stamen Toner")
)
select_data = st.sidebar.radio(
    "What data do you want to see?",
    ("Total_Pop", "Area_Region","Male_Pop",'Female_Pop')
)

map_sby = folium.Map(tiles=select_maps, location=[centers[0], centers[1]], zoom_start=12)
st.title('Map of Surabaya')

data_all['District'] = data_all['District'].str.title()
data_all = data_all.replace({'District':'Pabean Cantikan'},'Pabean Cantian')
data_all = data_all.replace({'District':'Karangpilang'},'Karang Pilang')

dicts = {"Total_Pop":'Total Population',
        "Male_Pop": 'Male Population',
        "Female_Pop": 'Female Population',
        "Area_Region": 'Areas Region(km squared)'}

for idx in range(31):
    data_geo['features'][idx]['properties']['Total_Pop'] = int(data_all['Total Population'][idx])
    data_geo['features'][idx]['properties']['Male_Pop'] = int(data_all['Male Population'][idx])
    data_geo['features'][idx]['properties']['Female_Pop'] = int(data_all['Female Population'][idx])
    data_geo['features'][idx]['properties']['Area_Region'] = float(data_all['Areas Region(km squared)'][idx])

show_maps(select_data, threshold(select_data))
