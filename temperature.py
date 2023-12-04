"""
Query temperature data from API
"""

import openmeteo_requests
import pandas as pd

def get_data(latitude, longitude, start_date, end_date):
    """
	Retrieve the temperature data for a particular location and time period

	Args:
		latitude (float): Between -90 and 90
		longitude (float): Between -180 and 180
		start_date (str): Starting date of temperature data
		end_date (str): Ending date of temperature data

	Returns:
		Dataframe containing daily temperature data for specified range
	"""
	# Create client for server request
    openmeteo = openmeteo_requests.Client()

    # Define requests URL and parameters
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
		"latitude": latitude,
		"longitude": longitude,
		"start_date": start_date,
		"end_date": end_date,
		"daily": "temperature_2m_mean"
	}

	# Request data
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

	# Process daily data
    daily = response.Daily()
    daily_temperature_2m_mean = daily.Variables(0).ValuesAsNumpy()

	# Create date range, insert temperature data into dataframe
    daily_dataframe = pd.DataFrame({
		"date": pd.date_range(start_date, end_date),
		"temperature": daily_temperature_2m_mean})

	# Calculate year and day of year from date
    daily_dataframe["doy"] = daily_dataframe["date"].dt.dayofyear
    daily_dataframe["year"] = daily_dataframe["date"].dt.year

    return daily_dataframe
