import logging
from datetime import datetime
from math import cos, radians
import math
import pymongo
from flask import Flask, jsonify, request
from pymongo import DESCENDING
import json
from bson import json_util
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="w",
    format="%(name)s-%(levelname)s-%(message)s",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)s-%(levelname)s-%(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://mongodb:27017")
db = myclient["kafka_db"]
mycol_wave = db["waveData"]
mycol_wind = db["windData"]
mycol_living = db['living_lab']  # Όνομα της συλλογής
mycol_dynamic = db["ais_cyprus_dynamic"]
mycol_static = db["ais_cyprus_static"]
mycol_other = db["ais_cyprus_other"]

@app.route('/lab', methods=['POST'])
def add_data():
    try:
        json_data = request.data
        data_str = json_data.decode('utf-8')
        pattern = r'"id":(\w+)'
        data_with_quotes = re.sub(pattern, lambda x: f'"id":"{x.group(1)}"', data_str)
        # data_with_quotes = json_data.replace(b'ID', b'"ID"')
        data_list = json.loads(data_with_quotes)
        logging.info(f'data_list: {data_list}')

        mycol_living.insert_many(data_list)
        return jsonify({'message': 'Data added successfully'})
    except Exception as e:
        logging.info(f'error: {str(e)}')
        return jsonify({'error': str(e)})
            

@app.route('/living_lab', methods=['GET'])
def get_living_lab_data():
    try:
        date_min = datetime.strptime(request.args.get("dateMin"), "%Y-%m-%dT%H:%M:%S")
        date_max = datetime.strptime(request.args.get("dateMax"), "%Y-%m-%dT%H:%M:%S")

        results = mycol_living.find({
            'formattedDate': {
                '$gte': date_min.strftime("%d/%m/%Y %H:%M:%S"),
                '$lte': date_max.strftime("%d/%m/%Y %H:%M:%S")
            }
        })

        data_list = list(results)
        json_data = json.loads(json_util.dumps(data_list))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)})


# def create_square(latitude, longitude, radius):
  
#     radius_in_degrees = radius / 111.00
#     min_latitude = latitude - radius_in_degrees
#     max_latitude = latitude + radius_in_degrees
#     min_longitude = longitude - radius_in_degrees
#     max_longitude = longitude + radius_in_degrees

#     return min_latitude, min_longitude, max_latitude, max_longitude

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
        
def search_data(
    start_date,
    end_date,
    min_longitude,
    max_longitude,
    min_latitude,
    max_latitude,
    database,
):
    query = {}
    # sort_order = [("time", DESCENDING)]
    # limit = 1
    # result = database.find(query).sort(sort_order).limit(limit)
    # date_format = "%Y-%m-%d %H:%M:%S"
    # most_recent_date = [
    #     datetime.strptime(document["time"], date_format) for document in result
    # ]

    # if min(most_recent_date) > end_date or max(most_recent_date) < start_date:
    #     return {database.name: []}
    # else:
            
    # start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
    # end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")
    # start_timestamp = start_date.timestamp()
    # end_timestamp = end_date.timestamp()
    logging.info(f'start time: {start_date}')
    logging.info(f'end: {end_date}')
            
    query = {
            "time": {"$gte": start_date, "$lte": end_date},
            "longitude": {"$gte": min_longitude, "$lte": max_longitude},
            "latitude": {"$gte": min_latitude, "$lte": max_latitude},
    }

    logging.info(f'query: {query}')
    last_data = database.find(query)

    if not last_data:
            logging.info(f'last_data: {list(last_data)}')
            return {database.name: []}
    else:
            data_list = []
            for document in last_data:
                data_list.append(document)
            for data in data_list:
                data.pop("_id", None)
            return {database.name: data_list}


@app.route("/data", methods=["GET"])
def get_data():
    latitude, longitude, radius = map(
        float,
        [
            request.args.get("latitude"),
            request.args.get("longitude"),
            request.args.get("radius"),
        ],
    )
    lat_min, lon_min, lat_max, lon_max = create_square(latitude,
                                                       longitude,
                                                       radius)

    date_format = "%Y-%m-%d %H:%M:%S"
    date_min = datetime.strptime(
        request.args.get("dateMin").replace("T", " "), date_format
    )
    date_max = datetime.strptime(
        request.args.get("dateMax").replace("T", " "), date_format
    )
    info_return = [
        search_data(date_min, date_max, lon_min,
                    lon_max, lat_min, lat_max, mycol_wave),
        search_data(date_min, date_max, lon_min,
                    lon_max, lat_min, lat_max, mycol_wind),
    ]
    return jsonify(info_return)


@app.route("/status12", methods=["GET"])
def get_status():
    api_is_up = True

    if api_is_up:
        response = {"status": "success"}
    else:
        response = {"status": "fail"}

    return jsonify(response)

@app.route("/ais_cyprus_dynamic", methods=["GET"])
def get_ais_cyprus_dynamic():
    try:
        results = mycol_dynamic.find()
        data_list = list(results)
        json_data = json.loads(json_util.dumps(data_list))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/ais_cyprus_static", methods=["GET"])
def get_ais_cyprus_static():
    try:
        results = mycol_static.find()
        data_list = list(results)
        json_data = json.loads(json_util.dumps(data_list))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/ais_cyprus_other", methods=["GET"])
def get_ais_cyprus_other():
    try:
        results = mycol_other.find()
        data_list = list(results)
        json_data = json.loads(json_util.dumps(data_list))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
