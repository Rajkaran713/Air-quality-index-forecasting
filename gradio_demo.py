import gradio as gr
from datetime import datetime
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


# Load the CSV file into a DataFrame
folder_path = os.path.dirname(os.path.abspath(__file__))
file_path = folder_path + "/LSTM_forecasted_values.csv"
df = pd.read_csv(file_path)

# Convert the Date column to the required format (YYYY-MM-DD)
df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

# Calculate AQI and categorize it
df["AQI"] = df.apply(calculate_aqi, axis=1)
df["Air Quality"] = df["AQI"].apply(categorize_aqi)

# Convert the DataFrame to a list of lists
data = df.apply(
    lambda row: [
        row["Date"],
        row["NO2"],
        row["O3"],
        row["PM2.5"],
        row["PM10"],
        row["AQI"],
        row["Air Quality"],
    ],
    axis=1,
).tolist()


def search_by_date(date_input):
    date_str = datetime.fromtimestamp(date_input).strftime("%Y-%m-%d")
    for row in data:
        if row[0] == date_str:
            return row[1], row[2], row[3], row[4], row[5], row[6]
    return "No data found", "", "", "", "", ""


interface = gr.Interface(
    fn=search_by_date,
    inputs=gr.DateTime(
        label="Select Date", include_time=False, timezone="America/Toronto"
    ),
    outputs=[
        gr.Textbox(label="NO2"),
        gr.Textbox(label="O3"),
        gr.Textbox(label="PM2.5"),
        gr.Textbox(label="PM10"),
        gr.Textbox(label="Air quality index"),
        gr.Textbox(label="Air quality"),
    ],
    title="Air Quality Prediction",
    description="Enter a date to retrieve air quality information.",
)

interface.launch()
