import streamlit as st
import requests
import datetime
import folium
from streamlit_folium import st_folium

# API url
api_url = st.secrets['API_URL']

# Page config layout
st.set_page_config(page_title = 'Taxifare Estimator', layout='wide')
st.header("TaxiFare Estimator")

# 1. Initialisation des coordonnées dans session_state
defaults = {
    "pickup_longitude": -73.9855,
    "pickup_latitude": 40.7580,
    "dropoff_longitude": -73.9712,
    "dropoff_latitude": 40.7769,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if "click_step" not in st.session_state:
    st.session_state.click_step = "pickup"  # alterne entre "pickup" et "dropoff"
if "last_clicked" not in st.session_state:
    st.session_state.last_clicked = None

# 2. Carte interactive pour choisir prise en charge puis dépose
st.subheader("Select pickup and dropoff locations")
st.caption(
    "Next click : **Pickup location**"
    if st.session_state.click_step == "pickup"
    else "Next click : **Dropoff location**"
)

m = folium.Map(
    location=[st.session_state.pickup_latitude, st.session_state.pickup_longitude],
    zoom_start=12,
)

folium.Marker(
    location=[st.session_state.pickup_latitude, st.session_state.pickup_longitude],
    popup="Pickup",
    icon=folium.Icon(color="green", icon="play"),
).add_to(m)

folium.Marker(
    location=[st.session_state.dropoff_latitude, st.session_state.dropoff_longitude],
    popup="Dropoff",
    icon=folium.Icon(color="red", icon="stop"),
).add_to(m)

folium.PolyLine(
    locations=[
        [st.session_state.pickup_latitude, st.session_state.pickup_longitude],
        [st.session_state.dropoff_latitude, st.session_state.dropoff_longitude],
    ],
    color="blue",
    weight=3,
    dash_array="5, 5",
).add_to(m)

map_data = st_folium(m, height=420, use_container_width=True)

# 3. Mise à jour des coordonnées lors d'un clic sur la carte
if map_data and map_data.get("last_clicked"):
    lat = float(map_data["last_clicked"]["lat"])
    lng = float(map_data["last_clicked"]["lng"])
    clicked = (lat, lng)

    if clicked != st.session_state.last_clicked:
        st.session_state.last_clicked = clicked

        if st.session_state.click_step == "pickup":
            st.session_state.pickup_latitude = lat
            st.session_state.pickup_longitude = lng
            st.session_state.click_step = "dropoff"
        else:
            st.session_state.dropoff_latitude = lat
            st.session_state.dropoff_longitude = lng
            st.session_state.click_step = "pickup"

        st.rerun()

# 4. Récupération des coordonnées depuis session_state + reste de votre logique intact
pickup_longitude = st.session_state.pickup_longitude
pickup_latitude = st.session_state.pickup_latitude
dropoff_longitude = st.session_state.dropoff_longitude
dropoff_latitude = st.session_state.dropoff_latitude

col1, col2 = st.columns(2)
with col1:
    st.caption(f"Pickup : `{pickup_latitude:.5f}`, `{pickup_longitude:.5f}`")
with col2:
    st.caption(f"Dropoff : `{dropoff_latitude:.5f}`, `{dropoff_longitude:.5f}`")

st.subheader('Select pickup date')
pickup_datetime = st.datetime_input("Pickup Datetime")

st.subheader('Select passengers count')
passenger_count = st.number_input("Passengers", 1, 3)




# pickup_datetime = st.datetime_input('Pickup Datetime')
# pickup_longitude = st.slider('Pickup Longitude', min_value=-180.0, max_value=180.0)
# pickup_latitude = st.slider('Pickup Latitude', min_value=-90.0, max_value=90.0)
# dropoff_longitude = st.slider('Dropoff Longitude', min_value=-180.0, max_value=180.0)
# dropoff_latitude = st.slider('Dropoff Latitude', min_value=-90.0, max_value=90.0)
# passenger_count = st.number_input('Passengers', 1, 3)

if st.button("Predict fare"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count,
    }

    response = requests.get(f"{api_url}/predict", params=params).json()
    st.write(response['fare'])
