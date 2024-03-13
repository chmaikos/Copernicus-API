import json
import math
import os
import time
from datetime import datetime, timedelta

import motuclient
import numpy as np
import pandas as pd
from config import settings
from confluent_kafka import Producer
from database import db
from netCDF4 import Dataset, num2date


def create_square(lat1, lon1, distance_km):
    R = 6371.0  # Radius of the Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    bearing_list_lat = [0, 180]
    bearing_list_lon = [90, 270]  # τα διαφορετικα

    # Convert bearing from degrees to radians
    bearing_90 = math.radians(bearing_list_lon[0])
    bearing_270 = math.radians(bearing_list_lon[1])
    bearing_0 = math.radians(bearing_list_lat[0])
    bearing_180 = math.radians(bearing_list_lat[1])

    # Calculate new latitude
    lat2_0 = math.asin(
        math.sin(lat1) * math.cos(distance_km / R)
        + math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_0)
    )

    # Calculate new latitude
    lat2_180 = math.asin(
        math.sin(lat1) * math.cos(distance_km / R)
        + math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_180)
    )

    # Calculate new latitude
    lat2_90 = math.asin(
        math.sin(lat1) * math.cos(distance_km / R)
        + math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_90)
    )

    # Calculate new latitude
    lat2_270 = math.asin(
        math.sin(lat1) * math.cos(distance_km / R)
        + math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_270)
    )

    # Calculate new longitude
    lon2_90 = lon1 + math.atan2(
        math.sin(bearing_90) * math.sin(distance_km / R) * math.cos(lat1),
        math.cos(distance_km / R) - math.sin(lat1) * math.sin(lat2_90),
    )

    # Calculate new longitude
    lon2_270 = lon1 + math.atan2(
        math.sin(bearing_270) * math.sin(distance_km / R) * math.cos(lat1),
        math.cos(distance_km / R) - math.sin(lat1) * math.sin(lat2_270),
    )

    # Convert latitude and longitude back to degrees
    lat2_0 = math.degrees(lat2_0)
    lat2_180 = math.degrees(lat2_180)
    lon2_90 = math.degrees(lon2_90)
    lon2_270 = math.degrees(lon2_270)

    return lat2_180, lon2_270, lat2_0, lon2_90


class MotuOptions:
    def __init__(self, attrs: dict):
        super(MotuOptions, self).__setattr__("attrs", attrs)

    def __setattr__(self, k, v):
        self.attrs[k] = v

    def __getattr__(self, k):
        try:
            return self.attrs[k]
        except KeyError:
            return None


def motu_option_parser(script_template, usr, pwd, PROD_WAVE_OUTPUT_FILENAME):
    dictionary = dict(
        [e.strip().partition(" ")[::2] for e in script_template.split("--")]
    )
    dictionary["variable"] = [
        value
        for (var, value) in [
            e.strip().partition(" ")[::2] for e in script_template.split("--")
        ]
        if var == "variable"
    ]
    for k, v in list(dictionary.items()):
        if v == "<OUTPUT_DIRECTORY>":
            dictionary[k] = "."
        if v == "<PROD_WAVE_OUTPUT_FILENAME>":
            dictionary[k] = PROD_WAVE_OUTPUT_FILENAME
        if v == "<USERNAME>":
            dictionary[k] = usr
        if v == "<PASSWORD>":
            dictionary[k] = pwd
        if k in [
            "longitude-min",
            "longitude-max",
            "latitude-min",
            "latitude-max",
            "depth-min",
            "depth-max",
        ]:
            dictionary[k] = float(v)
        if k in ["date-min", "date-max"]:
            dictionary[k] = v[1:-1]
        dictionary[k.replace("-", "_")] = dictionary.pop(k)
    dictionary.pop("python")
    dictionary["auth_mode"] = "cas"
    return dictionary


producer = Producer(settings.KAFKA_PRODUCER_CONFIG)
topic = settings.WAVE_TOPIC


def process_and_publish_wave_data():
    mycol = db["waveData"]
    lon = settings.DEFAULT_LONGITUDE
    lat = settings.DEFAULT_LATITUDE
    rad = settings.DEFAULT_RADIUS

    lat_min, lon_min, lat_max, lon_max = create_square(lat, lon, rad)

    curr_time = datetime.now() - timedelta(days=2)
    delta_3h = curr_time - timedelta(hours=3) + timedelta(seconds=1)
    mycol.drop()

    USERNAME = settings.USERNAME
    PASSWORD = settings.PASSWORD
    PROD_WAVE_OUTPUT_FILENAME = settings.PROD_WAVE_OUTPUT_FILENAME

    script_template = (
        f'python -m motuclient \
        --motu https://nrt.cmems-du.eu/motu-web/Motu \
        --service-id GLOBAL_ANALYSISFORECAST_WAV_001_027-TDS \
        --product-id cmems_mod_glo_wav_anfc_0.083deg_PT3H-i \
        --longitude-min {lon_min} --longitude-max {lon_max} \
        --latitude-min {lat_min} --latitude-max {lat_max} \
        --date-min "'
        + str(delta_3h)
        + '" --date-max "'
        + str(curr_time)
        + '" \
        --variable VHM0 --variable VMDR --variable VTM10 \
        --out-dir <OUTPUT_DIRECTORY> --out-name <PROD_WAVE_OUTPUT_FILENAME> \
        --user <USERNAME> --pwd <PASSWORD>'
    )

    data_request_options_dict_automated = motu_option_parser(
        script_template, USERNAME, PASSWORD, PROD_WAVE_OUTPUT_FILENAME
    )

    # Assuming motuclient setup remains as is
    motuclient.motu_api.execute_request(
        MotuOptions(data_request_options_dict_automated)
    )

    waveData = Dataset(PROD_WAVE_OUTPUT_FILENAME, "r+")
    waveData.set_auto_mask(True)

    # Extract variables for wave dataset
    vhm0 = waveData.variables["VHM0"]
    vmdr = waveData.variables["VMDR"]
    vtm10 = waveData.variables["VTM10"]

    # Get dimensions assuming 3D: time, latitude, longitude
    time_dim, lat_dim, lon_dim = vhm0.get_dims()
    time_var = waveData.variables[time_dim.name]
    times = num2date(time_var[:], time_var.units)
    latitudes = waveData.variables[lat_dim.name][:]
    longitudes = waveData.variables[lon_dim.name][:]

    times_grid, latitudes_grid, longitudes_grid = [
        x.flatten() for x in np.meshgrid(times, latitudes, longitudes, indexing="ij")
    ]

    df = pd.DataFrame(
        {
            "time": [t.isoformat(sep=" ") for t in times_grid],
            "latitude": latitudes_grid,
            "longitude": longitudes_grid,
            "vhm0": vhm0[:].flatten(),
            "vmdr": vmdr[:].flatten(),
            "vtm10": vtm10[:].flatten(),
        }
    )

    df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S")
    df["location"] = df.apply(
        lambda row: {
            "type": "Point",
            "coordinates": [row["longitude"], row["latitude"]],
        },
        axis=1,
    )

    df.drop(columns=["latitude", "longitude"], inplace=True)

    # Drop rows with null values in 'vhm0'
    df = df.dropna(subset=["vhm0"])

    # Convert DataFrame to a list of dictionaries (JSON-like documents)
    data = df.to_dict(orient="records")

    mycol.insert_many(data)

    # Convert it back to string format
    df["time"] = df["time"].dt.strftime("%Y-%m-%d %H:%M:%S")

    for _, row in df.iterrows():
        data_topic = row.to_dict()
        value = json.dumps(data_topic).encode("utf-8")
        producer.produce(topic=topic, value=value)
        producer.flush()
    file_path = PROD_WAVE_OUTPUT_FILENAME
    try:
        os.remove(file_path)
    except Exception as e:
        print(e)
    time.sleep(3 * 3600)
