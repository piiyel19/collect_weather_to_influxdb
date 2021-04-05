import requests, json

from influxdb import InfluxDBClient,DataFrameClient
from datetime import datetime,date,timedelta

client = InfluxDBClient(host='localhost', port=8086, database='your_databases')

def collect_data_openweather(city):
    api_key = "{key_id}"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    
    if x["cod"] != "404":
        y = x["main"]
        
        current_temperature = y["temp"]
        celsius = float(current_temperature)-float(273.15)

        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        
        z = x["weather"]
        weather_description = z[0]["description"]

        weather=z = x["weather"][0]["main"]

        save_database(current_temperature,celsius,current_pressure,current_humidiy,weather_description,weather)

    return ''


def save_database(current_temperature,celsius,current_pressure,current_humidiy,weather_description,weather):
    from datetime import datetime
    import pytz


    UTC_datetime_format = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    dateTimeObj = datetime.now()

    #print(dateTimeObj)
   # print(local_datetime_converted)

    json_body = [
        {
            "measurement": "weather_tumpat",
            "tags": {
                "host": "localhost",
                "region": "us-west"
            },
            #"time": UTC_datetime_format,
            "fields": {
                "weather":weather,
                "kelvin_temp": current_temperature,
                "celsius_temp": celsius,
                "pressure": current_pressure,
                "humidiy": current_humidiy,
                "weather_description": weather_description,
                "time_system":str(dateTimeObj)
            }
        }
    ]

    client.write_points(json_body)

    print(json_body)
    return ''


print(collect_data_openweather('Tumpat, Kelantan'))
