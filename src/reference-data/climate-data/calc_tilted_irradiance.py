import pandas as pd
from pvlib.irradiance import get_total_irradiance
from pvlib.solarposition import get_solarposition

# Розрахунок інсоляції на вертикальні поверхні
def calc_tilted_irradiance(csv_file):
    # Завантаження даних із CSV
    header = pd.read_csv(csv_file, nrows=1)
    df = pd.read_csv(csv_file, skiprows=2)

    # Встановлення координат (широта, довгота)
    latitude = header['Latitude'].values[0]
    longitude = header['Longitude'].values[0]

    # Створення тимчасової мітки на основі даних
    df['datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute']])

    # Перетворення datetime в індекс
    df = df.set_index('datetime')
    df.index = df.index - pd.DateOffset(hours=2) # Приведення даних в локальному часі до UTC

    # Розрахунок положення сонця (перший аргумент - це pandas.DatetimeIndex)
    solar_position = get_solarposition(df.index, latitude, longitude)

    # Додавання даних положення сонця до таблиці
    df['apparent_zenith'] = solar_position['apparent_zenith']
    df['azimuth'] = solar_position['azimuth']

    # Визначення параметрів для напрямків (північ, північний схід тощо)
    orientations = {
        'north': 0,
        'northeast': 45,
        'east': 90,
        'southeast': 135,
        'south': 180,
        'southwest': 225,
        'west': 270,
        'northwest': 315
    }

    # Функція для розрахунку інсоляції на похилій поверхні
    def calculate_irradiance(df, tilt, azimuth):
        surface_irradiance = get_total_irradiance(
            surface_tilt=tilt,
            surface_azimuth=azimuth,
            dni=df['DNI'],
            ghi=df['GHI'],
            dhi=df['DHI'],
            solar_zenith=df['apparent_zenith'],
            solar_azimuth=df['azimuth'],
            albedo=0 # Приймаємо альбедо рівному 0, для виключення із розрахунку відбитого випромінювання
        )
        return surface_irradiance['poa_global']

    # Додавання розрахунків для кожного напряму
    tilt = 90  # Вертикальні поверхні
    for direction, azimuth in orientations.items():
        df[f'irradiance_{direction}'] = calculate_irradiance(df, tilt, azimuth)

    # Виведення результатів у CSV
    df.to_csv(csv_file, index=False)

    print(f'Data has been saved to {csv_file}')
