# from datetime import datetime
# from math import cos, radians
# import logging
# import pymongo
# from flask import Flask, jsonify, request
# from pymongo import DESCENDING

# # Configure logging
# logging.basicConfig(level=logging.INFO, filename='app.log',
#                     filemode='w', format='%(name)s-%(levelname)s-%(message)s')
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)s-%(levelname)s-%(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)

# app = Flask(__name__)

# myclient = pymongo.MongoClient("mongodb://mongodb:27017")
# db = myclient["kafka_db"]
# mycol_wave = db["waveData"]
# mycol_wind = db["windData"]


# def create_square(latitude, longitude, radius):
#     earth_radius = 6371.0
#     lat_rad = radians(latitude)
#     radius_deg = radius / earth_radius
#     min_latitude = latitude - radius_deg
#     max_latitude = latitude + radius_deg
#     min_longitude = longitude - (radius_deg / cos(lat_rad))
#     max_longitude = longitude + (radius_deg / cos(lat_rad))
#     return min_latitude, min_longitude, max_latitude, max_longitude


# def search_data(start_date, end_date,
#                 min_longitude, max_longitude,
#                 min_latitude, max_latitude,
#                 database):
#     query = {}
#     sort_order = [("time", DESCENDING)]
#     limit = 1
#     result = database.find(query).sort(sort_order).limit(limit)
#     logging.info(f'result: {result[0]}')
#     date_format = "%Y-%m-%d %H:%M:%S"
#     most_recent_date = [datetime.strptime(document['time'], date_format)
#                         for document in result]
#     # logging.info(f'most_recent_date: {most_recent_date}')
#     # logging.info(f'end_date: {end_date}')
#     # logging.info(f'start_date: {start_date}')
#     if len(list(most_recent_date)) == 0 :
#         return {database.name: []}
#     if min(most_recent_date) > end_date or max(most_recent_date) < start_date:
#         # logging.info(f'1o if where we calculate the date')
#         return {database.name: []}
#     else:
#         # logging.info(f'min_longitude: {min_longitude} max_longitude: {max_longitude}')
#         # logging.info(f'min_latitude: {min_latitude} max_latitude: {max_latitude}')
#         # Convert provided date to datetime object
#         # Convert it to a string
#         start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
#         end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")
#         logging.info(f'start time: {start_date_str}')
#         logging.info(f'end: {end_date_str}')
        
#         query = {
#             # "time": {"$gte": start_date_str, "$lte": end_date_str},
#             "longitude": {"$gte": min_longitude, "$lte": max_longitude},
#             "latitude": {"$gte": min_latitude, "$lte": max_latitude}
#         }
      
#         logging.info(f"Query: {query}")

#         # Assuming 'mycol_wave' is your collection
#         sample_document = database.find_one()
        
#         # Assuming 'time' is the field where the date is stored
#         sample_date = sample_document['time']
        
#         # Print the sample date
#         logging.info(f"Sample Date: {sample_document}")

#         last_data = database.find(query)

#         if len(list(last_data)) == 0:
#             # logging.info(f'2o if where we calculate the lon and lat')
#             return {database.name: []}
#         else:
#             data_list = []
#             # logging.info(f'last_data: {last_data}')
#             for document in last_data:
#                 # logging.info(f'data: {document}')
#                 data_list.append(document)
#             # data_list = [doc for doc in last_data]
#             # logging.info(f'data_list: {data_list}')
#             for data in data_list:
#                 data.pop("_id", None)
#             return {database.name: data_list}


# @app.route('/data', methods=['GET'])
# def get_data():
#     latitude, longitude, radius = map(float, [request.args.get('latitude'),
#                                               request.args.get('longitude'),
#                                               request.args.get('radius')])
#     lat_min, lon_min, lat_max, lon_max = create_square(latitude,
#                                                        longitude,
#                                                        radius)

#     date_format = "%Y-%m-%d %H:%M:%S"
#     date_min = datetime.strptime(request.args.get('dateMin').replace('T', ' '),
#                                  date_format)
#     date_max = datetime.strptime(request.args.get('dateMax').replace('T', ' '),
#                                  date_format)
#     info_return = [
#         search_data(date_min, date_max,
#                     lon_min, lon_max,
#                     lat_min, lat_max,
#                     mycol_wave),
#         search_data(date_min, date_max,
#                     lon_min, lon_max,
#                     lat_min, lat_max,
#                     mycol_wind)
#     ]
#     return jsonify(info_return)

# @app.route('/status', methods=['GET'])
# def get_status():

#     api_is_up = True
    
#     if api_is_up:
#         response = {'status': 'success'}
#     else:
#         response = {'status': 'fail'}
    
#     return jsonify(response)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
