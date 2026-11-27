import streamlit as st
import requests
import datetime

"""
User interface of the taxifare estimator
"""

api_url = st.secrets['API_URL']

st.markdown("""# Taxifare
This is the taxifare estimator interface""")

# col1, col2 = st.columns(2)

# with col1:
pickup_datetime = st.datetime_input('Pickup Datetime')
pickup_longitude = st.slider('Pickup Longitude', min_value=-180.0, max_value=180.0)
pickup_latitude = st.slider('Pickup Latitude', min_value=-90.0, max_value=90.0)
dropoff_longitude = st.slider('Dropoff Longitude', min_value=-180.0, max_value=180.0)
dropoff_latitude = st.slider('Dropoff Latitude', min_value=-90.0, max_value=90.0)
passenger_count = st.number_input('Passengers', 1, 3)

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
