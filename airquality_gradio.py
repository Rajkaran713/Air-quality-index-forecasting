# -*- coding: utf-8 -*-
"""airquality_gradio

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BPKjX6HVqa6vVXYz_6b2YbzgLyPzjND8
"""

import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt


historical_data = pd.read_csv('/path/to/historical_data.csv')
forecast_data = pd.read_csv('/path/to/forecast_data.csv')

# Extract historical data
no2_data = historical_data.set_index('Date')['NO2']
o3_data = historical_data.set_index('Date')['O3']
pm10_data = historical_data.set_index('Date')['PM10']
pm25_data = historical_data.set_index('Date')['PM2.5']

# Extract forecast data
forecast_no2 = forecast_data.set_index('Date')['NO2']
forecast_o3 = forecast_data.set_index('Date')['O3']
forecast_pm10 = forecast_data.set_index('Date')['PM10']
forecast_pm25 = forecast_data.set_index('Date')['PM2.5']

def plot_predictions(pollutant):
    if pollutant == 'NO2':
        data = no2_data
        forecast = forecast_no2
    elif pollutant == 'O3':
        data = o3_data
        forecast = forecast_o3
    elif pollutant == 'PM10':
        data = pm10_data
        forecast = forecast_pm10
    elif pollutant == 'PM2.5':
        data = pm25_data
        forecast = forecast_pm25
    else:
        return "Invalid pollutant"

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data, label='Actual')
    plt.plot(forecast.index, forecast, label='Forecast', color='orange')
    plt.title(f'{pollutant} Predictions for the next 60 days')
    plt.xlabel('Date')
    plt.ylabel(pollutant)
    plt.legend()
    plt.grid(True)

    # Save the plot to a file
    plt.savefig('forecast_plot.png')
    plt.close()

    return 'forecast_plot.png'

# Create Gradio interface
iface = gr.Interface(
    fn=plot_predictions,
    inputs=gr.inputs.Dropdown(['NO2', 'O3', 'PM10', 'PM2.5'], label="Select Pollutant"),
    outputs=gr.outputs.Image(type="file", label="Forecast Plot"),
    title="Air Quality Forecasting",
    description="Select a pollutant to see the 60-day forecast based on the ARIMA model"
)

# Launch the interface
iface.launch()