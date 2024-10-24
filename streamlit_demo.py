import streamlit as st
import pandas as pd
import numpy as np
import os

# Define breakpoints for each pollutant
breakpoints = {
    "PM2.5": [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ],
    "PM10": [
        (0, 54, 0, 50),
        (55, 154, 51, 100),
        (155, 254, 101, 150),
        (255, 354, 151, 200),
        (355, 424, 201, 300),
        (425, 504, 301, 400),
        (505, 604, 401, 500),
    ],
    "NO2": [
        (0, 53, 0, 50),
        (54, 100, 51, 100),
        (101, 360, 101, 150),
        (361, 649, 151, 200),
        (650, 1249, 201, 300),
        (1250, 1649, 301, 400),
        (1650, 2049, 401, 500),
    ],
    "O3": [
        (0.000, 0.054, 0, 50),
        (0.055, 0.070, 51, 100),
        (0.071, 0.085, 101, 150),
        (0.086, 0.105, 151, 200),
        (0.106, 0.200, 201, 300),
    ],
}


# Function to calculate sub-index for a given pollutant
def calc_sub_index(concentration, breakpoints):
    for C_lo, C_hi, I_lo, I_hi in breakpoints:
        if C_lo <= concentration <= C_hi:
            return ((I_hi - I_lo) / (C_hi - C_lo)) * (concentration - C_lo) + I_lo
    return np.nan


# Function to calculate AQI from pollutant concentrations
def calculate_aqi(row):
    sub_indices = []
    for pollutant in ["PM2.5", "PM10", "NO2", "O3"]:
        sub_index = calc_sub_index(row[pollutant], breakpoints[pollutant])
        sub_indices.append(sub_index)
    return max(sub_indices)


# Add a new column to categorize AQI
def categorize_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy"
    else:
        return "Very Unhealthy"


# Load the CSV file into a DataFrameDataFrame
folder_path = os.path.dirname(os.path.abspath(__file__))
file_path = folder_path + "/ARIMA_forecasted_values.csv"
df = pd.read_csv(file_path)

# Convert the Date column to the required format (YYYY-MM-DD)
df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

# Calculate AQI and categorize it
df["AQI"] = df.apply(calculate_aqi, axis=1)
df["Air Quality"] = df["AQI"].apply(categorize_aqi)

# Streamlit UI
st.title("Air Quality Prediction")

# User selects a date
date_input = st.date_input("Select Date")

# Convert date_input to string format
date_str = date_input.strftime("%Y-%m-%d")

# Search for the date in the data
if date_str in df["Date"].values:
    selected_row = df[df["Date"] == date_str].iloc[0]
    st.write(f"**Date**: {selected_row['Date']}")
    st.write(f"**NO2**: {selected_row['NO2']}")
    st.write(f"**O3**: {selected_row['O3']}")
    st.write(f"**PM2.5**: {selected_row['PM2.5']}")
    st.write(f"**PM10**: {selected_row['PM10']}")
    st.write(f"**Air Quality Index (AQI)**: {selected_row['AQI']}")
    st.write(f"**Air Quality**: {selected_row['Air Quality']}")
else:
    st.write("No data found for the selected date.")
