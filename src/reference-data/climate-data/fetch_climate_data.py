import os
import requests
import urllib.parse
import time
import json
from dotenv import load_dotenv
from calc_tilted_irradiance import calc_tilted_irradiance

# Завантажуємо змінні оточенні з .env файлу
load_dotenv()

# Отримуємо шлях до директорії, де знаходиться поточний скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))

API_KEY = os.getenv('NSRDB_API_KEY')
EMAIL = os.getenv('EMAIL')
BASE_URL = "https://developer.nrel.gov/api/nsrdb/v2/solar/nsrdb-msg-v1-0-0-tmy-download.csv"

# Завантажуємо дані про міста з JSON-файлу
with open(os.path.join(script_dir, '../cities.json'), 'r', encoding='utf-8') as file:
    cities_data = json.load(file)

# Фільтруємо міста з координатами
cities = {city['city']: city['location'] for city in cities_data if city['location']}

# Назва піддиректорії для збереження результатів
output_directory = os.path.join(script_dir, 'cities')

# Створюємо піддиректорію якщо ії не існує
os.makedirs(output_directory, exist_ok=True)

# Основна функція для виконання запитів
def fetch_and_save_data():
    total_cities = len(cities)
    for index, (city, coordinates) in enumerate(cities.items(), start=1):
        params = {
            'api_key': API_KEY,
            'wkt': coordinates,
            'attributes': 'ghi,dni,dhi',
            'names': 'tmy',
            'utc': 'false',
            'leap_day': 'true',
            'interval': '60',
            'email': EMAIL
        }

        # Кодування параметрів URL
        url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
        response = requests.get(url)

        if response.status_code == 200:
            file_name = os.path.join(output_directory, f"{city.lower()}.csv")
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Data for {city} saved to {file_name}")

            # Обробка завантаженого файлу
            calc_tilted_irradiance(file_name)

        else:
            print(f"Error fetching data for {city}: {response.status_code} - {response.text}")

        # Вивід прогресу в консоль
        print(f"Processed {index} of {total_cities} cities...")

        # Затримка між запитами
        time.sleep(1)

if __name__ == "__main__":
    fetch_and_save_data()
