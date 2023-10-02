from datetime import datetime
from math import cos, radians
import logging
import pymongo
from flask import Flask, jsonify, request
from pymongo import DESCENDING

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log',
                    filemode='w', format='%(name)s-%(levelname)s-%(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s-%(levelname)s-%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://mongodb:27017")
db = myclient["kafka_db"]
mycol_wave = db["waveData"]
mycol_wind = db["windData"]


def create_square(latitude, longitude, radius):
    earth_radius = 6371.0
    lat_rad = radians(latitude)
    radius_deg = radius / earth_radius
    min_latitude = latitude - radius_deg
    max_latitude = latitude + radius_deg
    min_longitude = longitude - (radius_deg / cos(lat_rad))
    max_longitude = longitude + (radius_deg / cos(lat_rad))
    return min_latitude, min_longitude, max_latitude, max_longitude


def search_data(start_date, end_date,
                min_longitude, max_longitude,
                min_latitude, max_latitude,
                database):
    query = {}
    sort_order = [("time", DESCENDING)]
    limit = 1
    result = database.find(query).sort(sort_order).limit(limit)
    logging.info(f'result: {result[0]}')
    date_format = "%Y-%m-%d %H:%M:%S"
    most_recent_date = [datetime.strptime(document['time'], date_format)
                        for document in result]
    # logging.info(f'most_recent_date: {most_recent_date}')
    # logging.info(f'end_date: {end_date}')
    # logging.info(f'start_date: {start_date}')
    if len(list(most_recent_date)) == 0 :
        return {database.name: []}
    if min(most_recent_date) > end_date or max(most_recent_date) < start_date:
        # logging.info(f'1o if where we calculate the date')
        return {database.name: []}
    else:
        # logging.info(f'min_longitude: {min_longitude} max_longitude: {max_longitude}')
        # logging.info(f'min_latitude: {min_latitude} max_latitude: {max_latitude}')
        # Convert provided date to datetime object
        # Convert it to a string
        start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f'start time: {start_date_str}')
        logging.info(f'end: {end_date_str}')
        
        query = {
            # "time": {"$gte": start_date_str, "$lte": end_date_str},
            "longitude": {"$gte": min_longitude, "$lte": max_longitude},
            "latitude": {"$gte": min_latitude, "$lte": max_latitude}
        }
      
        logging.info(f"Query: {query}")

        # Assuming 'mycol_wave' is your collection
        sample_document = mycol_wave.find_one()
        
        # Assuming 'time' is the field where the date is stored
        sample_date = sample_document['time']
        
        # Print the sample date
        logging.info(f"Sample Date: {sample_document[0]}")

        last_data = database.find(query)

        if len(list(last_data)) == 0:
            # logging.info(f'2o if where we calculate the lon and lat')
            return {database.name: []}
        else:
            data_list = []
            # logging.info(f'last_data: {last_data}')
            for document in last_data:
                # logging.info(f'data: {document}')
                data_list.append(document)
            # data_list = [doc for doc in last_data]
            # logging.info(f'data_list: {data_list}')
            for data in data_list:
                data.pop("_id", None)
            return {database.name: data_list}


@app.route('/data', methods=['GET'])
def get_data():
    latitude, longitude, radius = map(float, [request.args.get('latitude'),
                                              request.args.get('longitude'),
                                              request.args.get('radius')])
    lat_min, lon_min, lat_max, lon_max = create_square(latitude,
                                                       longitude,
                                                       radius)

    date_format = "%Y-%m-%d %H:%M:%S"
    date_min = datetime.strptime(request.args.get('dateMin').replace('T', ' '),
                                 date_format)
    date_max = datetime.strptime(request.args.get('dateMax').replace('T', ' '),
                                 date_format)
    info_return = [
        search_data(date_min, date_max,
                    lon_min, lon_max,
                    lat_min, lat_max,
                    mycol_wave),
        search_data(date_min, date_max,
                    lon_min, lon_max,
                    lat_min, lat_max,
                    mycol_wind)
    ]
    return jsonify(info_return)

@app.route('/status', methods=['GET'])
def get_status():

    api_is_up = True
    
    if api_is_up:
        response = {'status': 'success'}
    else:
        response = {'status': 'fail'}
    
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
