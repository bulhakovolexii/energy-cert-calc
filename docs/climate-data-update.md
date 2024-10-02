# Завантаження або оновлення кліматичних даних

## Кліматичні дані

Дана модель використовує у якості вхідних даних, базу даних погодинних кліматичних величин
[NSRDB (National Solar Radiation Database)](https://nsrdb.nrel.gov/) "типового
метеорологічного року" (далі TMY).

> TMY означає «типовий метеорологічний рік» і є широко використовуваним типом даних,
> доступних через NSRDB. TMY містять погодинні дані за один рік, які найкраще
> представляють середні погодні умови за багаторічний період. Файл TMY створюється шляхом
> об’єднання 12 типових метеорологічних місяців зі статистично проаналізованих і вибраних
> окремих місяців із усього набору доступних років. Для вибору місяця TMY використовували
> десять індексів (див. таблицю). Індекси необхідні для вибору типового місяця з
> використанням вагового коефіцієнта для кожного параметра.

Завантаження даних відбувається безпосередньо з NDSRB по REST API, за наступним ендпойнтом.

> Meteosat Prime Meridian V1.0.0 TMY (/api/nsrdb/v2/solar/nsrdb-msg-v1-0-0-tmy-download)
>
> Зберіть і завантажте у форматі CSV конфігурований набір полів сонячних і метеорологічних
> даних із NSRDB. Національна база даних сонячного випромінювання (NSRDB) — це серійно
> повна колекція супутникових вимірювань сонячної радіації — глобального горизонтального,
> прямого нормального та дифузного горизонтального освітлення — і метеорологічних даних.
> Ці дані були зібрані в достатній кількості місць і в часових і просторових масштабах,
> щоб точно представити регіональний клімат сонячної радіації. Дані є загальнодоступними і
> безкоштовні для користувача. Ці API надають доступ до завантаження даних. Інші варіанти
> детально описані тут. Дізнайтеся більше про набори даних на https://nsrdb.nrel.gov.

[Деталі](https://developer.nrel.gov/docs/solar/nsrdb/nsrdb-msg-v1-0-0-tmy-download/)

Формат даних наступний:

- приклад запиту

`GET /api/nsrdb/v2/solar/nsrdb-msg-v1-0-0-download.csv?api_key={{API_KEY}}&wkt=POINT(-179.99 -15.94)&attributes=alpha,aod,ghi,dni,dhi&names=2019&utc=true&leap_day=true&interval=30&email=user@company.com`

- приклад відповіді

```
Source,Location ID,City,State,Country,Latitude,Longitude,Time Zone,Elevation,Local Time Zone,Clearsky DHI Units,Clearsky DNI Units,Clearsky GHI Units,Dew Point Units,DHI Units,DNI Units,GHI Units,Solar Zenith Angle Units,Temperature Units,Pressure Units,Relative Humidity Units,Precipitable Water Units,Wind Direction Units,Wind Speed,Cloud Type -15,Cloud Type 0,Cloud Type 1,Cloud Type 2,Cloud Type 3,Cloud Type 4,Cloud Type 5,Cloud Type 6,Cloud Type 7,Cloud Type 8,Cloud Type 9,Cloud Type 10,Cloud Type 11,Cloud Type 12,Fill Flag 0,Fill Flag 1,Fill Flag 2,Fill Flag 3,Fill Flag 4,Fill Flag 5,Surface Albedo Units,Version
NSRDB,0,-,b'None',b'None',-15.94,-179.99,0,0,12,w/m2,w/m2,w/m2,c,w/m2,w/m2,w/m2,Degree,c,mbar,%,cm,Degrees,m/s,N/A,Clear,Probably Clear,Fog,Water,Super-Cooled Water,Mixed,Opaque Ice,Cirrus,Overlapping,Overshooting,Unknown,Dust,Smoke,N/A,Missing Image,Low Irradiance,Exceeds Clearsky,Missing CLoud Properties,Rayleigh Violation,N/A,unknown
Year,Month,Day,Hour,Minute,Alpha,AOD,GHI,DNI,DHI
2019,1,1,0,0,1.02,0.0102,0,0,0
2019,1,1,0,45,1.02,0.0111,0,0,0
2019,1,1,1,30,1.02,0.0111,0,0,0
2019,1,1,2,15,1.04,0.0122,0,0,0
2019,1,1,3,0,1.06,0.013000000000000001,0,0,0
2019,1,1,3,45,1.07,0.0134,0,0,0
2019,1,1,4,30,1.07,0.0134,0,0,0
```

## Потрібно

Для оновлення кліматичних даних потрібно:

- `Python` версії `3.ХХ` із `pip` та набором бібліотек. (для перевірки скористуйтесь
  командами `python --version` та `pip --version`)
- API ключ NSRDB, детальніше про отримання [тут](https://developer.nrel.gov/signup/)

## Установка

1. Створіть в кореневій директорії проєкту віртуальне середовище

`python -m venv venv`

2. Активуйте його

Для windows:

- cmd.exe `venv\Scripts\activate.bat`
- PowerShell `venv\Scripts\Activate.ps1`

> Примітка У Microsoft Windows може знадобитися ввімкнути сценарій Activate.ps1,
> встановивши політику виконання для користувача. Ви можете зробити це, виконавши таку
> команду PowerShell:
> ```PS C:\> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```
> Додаткову інформацію див. у розділі 
[«Про політику виконання»](https://go.microsoft.com/fwlink/?LinkID=135170).

Для MacOS/Linux: `source venv/bin/activate`

3. Встановіть залежності `pip install pvlib python-dotenv`
4. Створіть в корені проєкту файл `.env` такого вмісу

```
NSRDB_API_KEY="Ваш API ключ NRSB"
EMAIL="Ваш E-mail"
```

5. Запустіть скрипт завантаження та обробки кліматичних даних

`python src/reference-data/climate-data/fetch_climate_data.py `

## Результат

Скрипт завантажить кліматичні дані для всіх обласних центрів України в
директорію `/src/reference-data/climate-data/cities`, та додасть до таблиць даних
відповідні таблиці із результатами розрахунків погодинних дози сумарної сонячної радіації,
осередненої для однієї години, що надходять на горизонтальну та вертикальну поверхні
різного орієнтування за поточних умов хмарності

Приклад вихідного файлу

```
Year,Month,Day,Hour,Minute,GHI,DNI,DHI,apparent_zenith,azimuth,irradiance_north,irradiance_northeast,irradiance_east,irradiance_southeast,irradiance_south,irradiance_southwest,irradiance_west,irradiance_northwest
2016,1,1,0,30,0,0,0,151.18704323447358,25.511524807806666,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
2016,1,1,1,30,0,0,0,145.28990924836805,49.41180018062272,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
2016,1,1,2,30,0,0,0,137.08323054443932,67.22342018344881,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
```
