import os
import logging
from netCDF4 import Dataset, num2date
import numpy as np
import pandas as pd
import cdsapi
import configparser
from datetime import datetime, timedelta
import time
import math
from math import pi, radians, cos
from confluent_kafka import Producer
import json
import pymongo
import metpy.calc as mpcalc
from metpy.units import units

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log',
                    filemode='w', format='%(name)s-%(levelname)s-%(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s-%(levelname)s-%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def delivery_report(err, msg):
    if err is not None:
        logging.error('Failed to deliver message: %s', err)
    else:
        logging.info('Message delivered to topic: %s', msg.topic())


def create_square(lat1, lon1, distance_km):
    R = 6371.0  # Radius of the Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    bearing_list_lat = [0, 180]
    bearing_list_lon = [90, 270] #τα διαφορετικα

    # Convert bearing from degrees to radians
    bearing_90 = math.radians(bearing_list_lon[0])
    bearing_270 = math.radians(bearing_list_lon[1])
    bearing_0 = math.radians(bearing_list_lat[0])
    bearing_180 = math.radians(bearing_list_lat[1])

    # Calculate new latitude
    lat2_0 = math.asin(math.sin(lat1) * math.cos(distance_km / R) +
                     math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_0))
    
    # Calculate new latitude
    lat2_180 = math.asin(math.sin(lat1) * math.cos(distance_km / R) +
                     math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_180))
    
     # Calculate new latitude
    lat2_90 = math.asin(math.sin(lat1) * math.cos(distance_km / R) +
                     math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_90))
    
    # Calculate new latitude
    lat2_270 = math.asin(math.sin(lat1) * math.cos(distance_km / R) +
                     math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_270))

    # Calculate new longitude
    lon2_90 = lon1 + math.atan2(math.sin(bearing_90) * math.sin(distance_km / R) * math.cos(lat1),
                             math.cos(distance_km / R) - math.sin(lat1) * math.sin(lat2_90))
    
    # Calculate new longitude
    lon2_270 = lon1 + math.atan2(math.sin(bearing_270) * math.sin(distance_km / R) * math.cos(lat1),
                             math.cos(distance_km / R) - math.sin(lat1) * math.sin(lat2_270))

    # Convert latitude and longitude back to degrees
    lat2_0 = math.degrees(lat2_0)
    lat2_180 = math.degrees(lat2_180)
    lon2_90 = math.degrees(lon2_90)
    lon2_270 = math.degrees(lon2_270)

    return lat2_180, lon2_270, lat2_0, lon2_90


producer = Producer({'bootstrap.servers': 'kafka1:29092'})
topic_metadata = producer.list_topics()
topic_list = topic_metadata.topics
for topic in topic_list:
    logging.info("----------------------------------------------- %s", topic)
topic = 'wind_topic'
topic_weather = 'weather_topic'
myclient = pymongo.MongoClient("mongodb://mongodb:27017")
db = myclient["kafka_db"]
mycol = db["windData"]

mycolweather = db["weatherData"]
mycolweather.drop()

while True:
    try:
        config = configparser.ConfigParser()
        config.read('config.conf')
        lon, lat, rad = map(float,
                            [config.get('Default', 'longitude'),
                             config.get('Default', 'latitude'),
                             config.get('Default', 'radius')]
                            )
        lat_min, lon_min, lat_max, lon_max = create_square(lat, lon, rad)
        curr_time = datetime.now() - timedelta(days=6)
        mon_curr, day_curr = curr_time.strftime("%m"), curr_time.strftime("%d")
        c = cdsapi.Client()
        windData = 'data/ERA5_Weather3H.nc'
        dataList = [{'fileLocation': windData,
                     'month': mon_curr,
                     'day': day_curr}]
        logging.info("month %s", dataList[0]["month"])
        logging.info("day %s", dataList[0]["day"])

        for item in dataList:
            c.retrieve('reanalysis-era5-single-levels',
                       {'product_type': 'reanalysis',
                        'variable': ['10m_u_component_of_wind',
                                     '10m_v_component_of_wind', 
                                     '2m_temperature', 
                                     '2m_dewpoint_temperature',
                                     'sea_surface_temperature',
                                     'total_cloud_cover', 
                                     'total_column_rain_water',
                                     'total_column_snow_water',
                                     'surface_pressure'
                                    ],
                        'year': '2024',
                        'month': item['month'],
                        'day': item['day'],
                        'time': [f'{i:02d}:00' for i in range(24)],
                        'area': [lat_max,
                                 lon_min,
                                 lat_min,
                                 lon_max],
                        'format': 'netcdf'},
                       item['fileLocation'])

        with Dataset('data/ERA5_Weather3H.nc', 'r+') as windData_BL:
            for var_name in windData_BL.variables.keys():
                variable = windData_BL.variables[var_name]
                logging.info(f'Variable Name: {var_name}')
                logging.info(f'Dimensions: {variable.dimensions}')
                logging.info(f'Shape: {variable.shape}')
                logging.info(f'Units: {variable.units if "units" in variable.ncattrs() else "N/A"}')
                logging.info(f'Description: {variable.long_name if "long_name" in variable.ncattrs() else "N/A"}')
                logging.info('\n')
            u10, v10, tem, dewpoint_temp, sea_temp, total_cloud_cover, total_rain_water, total_snow_water, pressure, = map(windData_BL.variables.get, ['u10', 'v10', 't2m', 'd2m', 'sst', 'tcc', 'tcrw', 'tcsw', 'sp'])
          
            logging.info(f'u10: {u10}')
            logging.info(f'v10: {v10}')
            logging.info(f'tem: {tem}')
            logging.info(f'dewpoint_temp: {dewpoint_temp}')
            logging.info(f'sea_temp: {sea_temp}')
            logging.info(f'total_cloud_cover: {total_cloud_cover}')
            logging.info(f'pressure: {pressure}')
            logging.info(f'total_rain_water: {total_rain_water}')
            logging.info(f'total_snow_water: {total_snow_water}')
          
            wind_speed = np.sqrt(u10[:]**2 + v10[:]**2)
            wind_dir = (270 - np.arctan2(v10[:], u10[:]) * 180 / pi) % 360
            time_dim, lat_dim, lon_dim = u10.get_dims()
            time_var = windData_BL.variables[time_dim.name]
            times = num2date(time_var[:], time_var.units)
            latitudes = windData_BL.variables[lat_dim.name][:]
            longitudes = windData_BL.variables[lon_dim.name][:]
            times_grid, latitudes_grid, longitudes_grid = [x.flatten()
                                                           for x
                                                           in np.meshgrid(
                                                               times,
                                                               latitudes,
                                                               longitudes,
                                                               indexing='ij')]

            if tem[:].flatten() is not None and dewpoint_temp[:].flatten() is not None:
              temp = tem[:].flatten()[0]
              dew = dewpoint_temp[:].flatten()[0]
              logging.info(f'tem: {temp}')
              logging.info(f'dew: {dew}')
              relative_humidity = mpcalc.relative_humidity_from_dewpoint(tem[:].flatten()[0] * units.degC, dewpoint_temp[:].flatten()[0] * units.degC)
            else:
              relative_humidity = 0

            df = pd.DataFrame({'time': [t.isoformat(sep=" ")
                                        for t in times_grid],
                               'latitude': latitudes_grid,
                               'longitude': longitudes_grid,
                               'u10': u10[:].flatten(),
                               'v10': v10[:].flatten(),
                               'speed': wind_speed.flatten(),
                               'direction': wind_dir.flatten()})

            df_weather = pd.DataFrame({'time': [t.isoformat(sep=" ") for t in times_grid],
                                     'latitude': latitudes_grid,
                                     'longitude': longitudes_grid,
                                     'temperature': tem[:].flatten(),
                                     'humidity': relative_humidity.magnitude * 100,
                                     'sea_temp': sea_temp[:].flatten(),
                                     'total_cloud_cover': total_cloud_cover[:].flatten() * 100,
                                     'pressure': pressure[:].flatten(),
                                     'total_rain_water': total_rain_water[:].flatten(),
                                     'total_snow_water': total_snow_water[:].flatten()})

          

            df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
            df_weather['time'] = pd.to_datetime(df_weather['time'], format='%Y-%m-%d %H:%M:%S')

            logging.info(df)
            logging.info(df_weather)
            df.dropna(subset=['u10'], inplace=True)
            df_weather.dropna(subset=['sea_temp'], inplace=True)
            logging.info(df)
            logging.info(df_weather)
            data = df.to_dict(orient='records')
            mycol.insert_many(data)
            data_weather = df_weather.to_dict(orient='records')
            mycolweather.insert_many(data_weather)

        # Convert it back to string format
        df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        for index, row in df.iterrows():
            value = json.dumps(row.to_dict()).encode('utf-8')
            producer.produce(topic=topic,
                             value=value,
                             callback=delivery_report)
            producer.flush()

        df_weather['time'] = df_weather['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        for index, row in df_weather.iterrows():
            value = json.dumps(row.to_dict()).encode('utf-8')
            producer.produce(topic=topic_weather,
                             value=value,
                             callback=delivery_report)
            producer.flush()

        os.remove(windData)
        logging.info("File deleted successfully.")
    except FileNotFoundError:
        logging.error("File not found.")
    except Exception as e:
        logging.error("Error: %s", e)
    time.sleep(24 * 60 * 60)
