import openmeteo_requests
import pandas as pd

start_date = "2003-01-01"
end_date = "2023-11-12"

def get_data():
	# Create client for server request
	openmeteo = openmeteo_requests.Client()

	# Define requests URL and parameters
	url = "https://archive-api.open-meteo.com/v1/archive"
	params = {
		"latitude": 42.2930153,
		"longitude": -71.2663569,
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