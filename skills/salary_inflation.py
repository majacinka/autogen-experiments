import os  
import requests  
from dotenv import load_dotenv  
  
# Load environment variables  
load_dotenv()  
  
# Retrieve the BLS API Key from the .env file  
BLS_API_KEY = os.getenv('BLS_API_KEY')  
  
# BLS API endpoint and headers  
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"  
headers = {"Content-Type": "application/json"}  
  
# Series ID for CPI-U (All Urban Consumers, not seasonally adjusted, all items)  
series_id = "CUUR0000SA0"  
  
# We want the last 5 years, so calculate the start year  
from_year = 2023 - 5  
  
# Prepare the payload for the API request  
payload = {  
    "seriesid": [series_id],  
    "startyear": str(from_year),  
    "endyear": "2023",  
    "registrationkey": BLS_API_KEY,  
}  
  
response = requests.post(url, json=payload, headers=headers)  
  
if response.status_code == 200:  
    data = response.json()  
    if data.get('status') == 'REQUEST_SUCCEEDED':  
        # Attempt to extract the December CPI values for each year  
        try:  
            cpi_values = [float(item['value']) for item in data['Results']['series'][0]['data'] if item['periodName'] == 'December']  
            cpi_values.reverse()  # Ensure the list is from past to present  
        except KeyError as e:  
            print("Failed to extract CPI values. KeyError:", e)  
            print("Data received:", data)  
            exit()  
  
        if not cpi_values or len(cpi_values) < 5:  
            print("Insufficient CPI values extracted. Check the series ID and the API response structure.")  
            exit()  
  
        # Calculate the cumulative inflation rate over the 5 years  
        initial_cpi = cpi_values[0]  
        current_cpi = cpi_values[-1]  
        inflation_rate = (current_cpi - initial_cpi) / initial_cpi  
  
        # Adjust the $50,000 salary for inflation  
        initial_salary = 50000  
        adjusted_salary = initial_salary * (1 + inflation_rate)  
  
        print(f"Adjusted salary for inflation over the last 5 years: ${adjusted_salary:.2f}")  
    else:  
        print("Failed to fetch data:", data.get('message'))  
else:  
    print("Failed to make request:", response.status_code)  