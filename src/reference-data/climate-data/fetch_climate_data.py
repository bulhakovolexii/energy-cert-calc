import os
import requests
import urllib.parse
import time
import json
from dotenv import load_dotenv
from calc_tilted_irradiance import calc_tilted_irradiance  # Импорт функции из второго скрипта

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем путь к директории, где находится текущий скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))

API_KEY = os.getenv('NSRDB_API_KEY')
EMAIL = os.getenv('EMAIL')
BASE_URL = "https://developer.nrel.gov/api/nsrdb/v2/solar/nsrdb-msg-v1-0-0-tmy-download.csv"

# Загружаем данные о городах из JSON-файла
with open(os.path.join(script_dir, '../cities.json'), 'r', encoding='utf-8') as file:
    cities_data = json.load(file)

# Фильтруем города с координатами
cities = {city['city']: city['location'] for city in cities_data if city['location']}

# Название поддиректории для сохранения данных
output_directory = os.path.join(script_dir, 'cities')

# Создаем поддиректорию, если она не существует
os.makedirs(output_directory, exist_ok=True)

# Основная функция для выполнения запросов
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

        # Кодирование параметров URL
        url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
        response = requests.get(url)

        if response.status_code == 200:
            file_name = os.path.join(output_directory, f"{city.lower()}.csv")
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Data for {city} saved to {file_name}")

            # Обработка загруженного файла
            calc_tilted_irradiance(file_name)

        else:
            print(f"Error fetching data for {city}: {response.status_code} - {response.text}")

        # Вывод прогресса
        print(f"Processed {index} of {total_cities} cities...")

        # Задержка между запросами
        time.sleep(1)

if __name__ == "__main__":
    fetch_and_save_data()
