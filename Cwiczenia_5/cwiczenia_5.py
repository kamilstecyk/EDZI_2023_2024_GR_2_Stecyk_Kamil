import requests
import pandas as pd
from datetime import datetime
import json

class WeatherData:
    def __init__(self, station_id, station_name, measurement_date, measurement_hour, temperature, wind_speed, wind_direction, humidity, precipitation, pressure):
        self.station_id = station_id
        self.station_name = station_name
        self.measurement_date = measurement_date
        self.measurement_hour = measurement_hour
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.humidity = humidity
        self.precipitation = precipitation
        self.pressure = pressure

    def __str__(self):
        return f"Station ID: {self.station_id}, Station Name: {self.station_name}, Measurement Date: {self.measurement_date}, Measurement Hour: {self.measurement_hour}, Temperature: {self.temperature}, Wind Speed: {self.wind_speed}, Wind Direction: {self.wind_direction}, Humidity: {self.humidity}, Precipitation: {self.precipitation}, Pressure: {self.pressure}"

def fetch_weather_data(station):
    headers = {
    'Content-Type': 'application/json; charset=utf-8'
    }

    url = f"https://danepubliczne.imgw.pl/api/data/synop/station/{station}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weather data for city with ID: {station}")
        return None
    
def convert_to_weather_data(data):
    return WeatherData(
        data["id_stacji"],
        data["stacja"],
        data["data_pomiaru"],
        data["godzina_pomiaru"],
        data["temperatura"],
        data["predkosc_wiatru"],
        data["kierunek_wiatru"],
        data["wilgotnosc_wzgledna"],
        data["suma_opadu"],
        data["cisnienie"]
    )

def save_array_to_excel(array):
    dicts = [vars(data) for data in array]
    df = pd.DataFrame(dicts)
    df.to_excel("weather_data.xlsx", index=False)
    print('Successfully saved data to excel file')

def save_array_to_json(array):
    dicts = [vars(data) for data in array]
    with open("weather_data.json", "w") as json_file:
        json.dump(dicts, json_file, indent=4, ensure_ascii=False)
        print('Successfully saved data to json file')

def display_and_save_weather_stats(df):
    avg_temperature = df['temperature'].mean().round(2)

    min_temp_index = df['temperature'].idxmin()
    min_temperature = df.loc[min_temp_index, 'temperature']
    min_temparature_location = df.loc[min_temp_index, 'station_name']

    max_temp_index = df['temperature'].idxmax()
    max_temperature = df.loc[max_temp_index, 'temperature']
    max_temparature_location = df.loc[max_temp_index, 'station_name']

    avg_precipitation = df['precipitation'].mean().round(2)

    min_precipitation_index = df['precipitation'].idxmin()
    min_precipitation = df.loc[min_precipitation_index, 'precipitation']
    min_precipitation_location = df.loc[min_precipitation_index, 'station_name']

    max_precipitation_index = df['precipitation'].idxmax()
    max_precipitation = df.loc[max_precipitation_index, 'precipitation']
    max_precipitation_location = df.loc[max_precipitation_index, 'station_name']

    avg_pressure = df['pressure'].mean().round(2)

    min_pressure_index = df['pressure'].idxmin()
    min_pressure = df.loc[min_pressure_index, 'pressure']
    min_pressure_location = df.loc[min_pressure_index, 'station_name']

    max_pressure_index = df['pressure'].idxmax()
    max_pressure = df.loc[max_pressure_index, 'pressure']
    max_pressure_location = df.loc[max_pressure_index, 'station_name']

    print("\n")
    print("Średnia temperatura punktów pomiarowych:", avg_temperature)
    print("Minimalna temperatura wraz z miejscem pomiaru:", min_temperature, ", ", min_temparature_location)
    print("Maksymalna temperatura wraz z miejscem pomiaru:", max_temperature, ', ', max_temparature_location)
    print("Data oraz godzina pomiaru: ", df.loc[0, 'measurement_date'], f"{df.loc[0, 'measurement_hour']}:00")
    print("Średnia wartość opadów:", avg_precipitation)
    print("Minimalna wartość opadów wraz z miejscem pomiaru:", min_precipitation, ', ', min_precipitation_location)
    print("Maksymalna wartość opadów wraz z miejscem pomiaru:", max_precipitation, ', ', max_precipitation_location)
    print("Średnia wartość ciśnienia:", avg_pressure)
    print("Minimalna wartość ciśnienia wraz z miejscem pomiaru:", min_pressure, ', ', min_pressure_location)
    print("Maksymalna wartość ciśnienia wraz z miejscem pomiaru:", max_pressure, ', ', max_pressure_location)

    results_dict = {
    "avg_temperature": avg_temperature,
    "min_temperature": min_temperature,
    "min_temperature_location": min_temparature_location,
    "max_temperature": max_temperature,
    "max_temperature_location": max_temparature_location,
    "measurement_datetime": f"{df.loc[0, 'measurement_date']} {df.loc[0, 'measurement_hour']}:00",
    "avg_precipitation": avg_precipitation,
    "min_precipitation": min_precipitation,
    "min_precipitation_location": min_precipitation_location,
    "max_precipitation": max_precipitation,
    "max_precipitation_location": max_precipitation_location,
    "avg_pressure": avg_pressure,
    "min_pressure": min_pressure,
    "min_pressure_location": min_pressure_location,
    "max_pressure": max_pressure,
    "max_pressure_location": max_pressure_location
    }

    # Zapis do pliku JSON
    with open('weather_data_raport.json', 'w') as json_file:
        json.dump(results_dict, json_file, indent=4, ensure_ascii=False)
        print('\nSuccessfully saved weather raport to json')

def main():
    cities = [
        'bialystok',
        'bydgoszcz',
        'gdansk',
        'gorzowwielkopolski',
        'katowice',
        'kielce',
        'krakow',
        'lublin',
        'lodz',
        'olsztyn',
        'opole',
        'poznan',
        'rzeszow',
        'szczecin',
        'torun',
        'warszawa',
        'wroclaw',
        'zielonagora'
    ]

    all_weather_data = []

    for city_name in cities:
        weather_data = fetch_weather_data(city_name)
        if weather_data:
            weather_data_converted = convert_to_weather_data(weather_data)
            all_weather_data.append(weather_data_converted)

    print(f'Got data for {len(all_weather_data)} cities')
    save_array_to_json(all_weather_data)

    data_dict_list = []
    for data in all_weather_data:
        data_dict = {
            'station_id': data.station_id,
            'station_name': data.station_name,
            'measurement_date': data.measurement_date,
            'measurement_hour': data.measurement_hour,
            'temperature': float(data.temperature),
            'wind_speed': float(data.wind_speed),
            'wind_direction': float(data.wind_direction),
            'humidity': float(data.humidity),
            'precipitation': float(data.precipitation),
            'pressure': float(data.pressure)
        }
        data_dict_list.append(data_dict)

    df = pd.DataFrame(data_dict_list)
    display_and_save_weather_stats(df)

if __name__ == "__main__":
    main()
