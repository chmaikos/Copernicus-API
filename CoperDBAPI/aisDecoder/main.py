from pyais.stream import UDPStream
import logging
import json
import pymongo
from pykafka import KafkaClient
from datetime import datetime

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

myclient = pymongo.MongoClient("mongodb://mongodb:27017")
db = myclient["kafka_db"]
mycol_dynamic = db["ais_cyprus_dynamic"]
mycol_static = db["ais_cyprus_static"]

kafka_client = KafkaClient(hosts='kafka1:29092')
kafka_producer_dynamic = kafka_client.topics[b'ais_cyprus_dynamic'].get_producer()
kafka_producer_static = kafka_client.topics[b'ais_cyprus_static'].get_producer()

host = "0.0.0.0"
port = 9094

while True:
    try:
        
        for msg in UDPStream(host, port):
            message = msg.decode()

            if message is not None:
                message_json = message.to_json()

                message_data = json.loads(message_json)
                message_type = message_data['decoded']['type']

                message_decoded = message_data['decoded']
                # logging.info(f'message: {message_decoded}')
                
                current_utc_time = datetime.utcnow()
                formatted_time = current_utc_time.strftime("%d/%m/%Y %H:%M:%S")

                new_data = {}
                new_data["timestamp"] = formatted_time
                
                if message_type in [1, 2, 3]:

                    message_decoded = message_data['decoded']
                    logging.info(f'message: {message_decoded}')

                    new_data["mmsi"] = message_decoded.get("mmsi")
                    new_data["nav_status"] = None
                    new_data["longitude"] = message_decoded.get("lon")
                    new_data["latitude"] = message_decoded.get("lat")
                    new_data["heading"] = message_decoded.get("heading")
                    new_data["sog"] = message_decoded.get("speed")
                    new_data["cog"] = message_decoded.get("course")
                    new_data["ais_type"] = message_decoded.get("type")

                    db.ais_cyprus_dynamic.insert_one(new_data)

                    
                    message_json = json.dumps(message_decoded)
                    message_bytes = message_json.encode('utf-8')
                    kafka_producer_dynamic.produce(message_bytes)
                    
                elif message_type in [9, 18]:

                    new_data["mmsi"] = message_decoded.get("mmsi")
                    new_data["nav_status"] = None
                    new_data["longitude"] = message_decoded.get("lon")
                    new_data["latitude"] = message_decoded.get("lat")
                    new_data["heading"] = message_decoded.get("heading")
                    new_data["sog"] = message_decoded.get("speed")
                    new_data["cog"] = message_decoded.get("course")
                    new_data["ais_type"] = message_decoded.get("type")
    
                    db.ais_cyprus_dynamic.insert_one(new_data)

                    message_json = json.dumps(message_decoded)
                    message_bytes = message_json.encode('utf-8')
                    kafka_producer_dynamic.produce(message_bytes)

                elif message_type == 5:

                    new_data["mmsi"] = message_decoded.get("mmsi")
                    new_data["imo"] = message_decoded.get("imo")
                    new_data["ship_name"] = message_decoded.get("shipname")
                    new_data["call_sign"] = message_decoded.get("callsign")
                    new_data["ship_type"] = message_decoded.get("shiptype")
                    new_data["draught"] = message_decoded.get("draught")
                    new_data["bow"] = message_decoded.get("to_bow")
                    new_data["stern"] = message_decoded.get("to_stern")
                    new_data["port"] = message_decoded.get("to_port")
                    new_data["starboard"] = message_decoded.get("to_starboard")
                    new_data["destination"] = message_decoded.get("destination")
                    new_data["ais_type"] = message_decoded.get("type")

                    db.ais_cyprus_static.insert_one(new_data)

                    message_json = json.dumps(message_decoded)
                    message_bytes = message_json.encode('utf-8')
                    kafka_producer_static.produce(message_bytes)

                elif message_type == 24 and message_decoded.get("to_port") is not None:

                    logging.info(f'message: {message_data}')

                    new_data["mmsi"] = message_decoded.get("mmsi")
                    new_data["imo"] = None
                    new_data["ship_name"] = None
                    new_data["call_sign"] = message_decoded.get("callsign")
                    new_data["ship_type"] = message_decoded.get("shiptype")
                    new_data["draught"] = None
                    new_data["bow"] = message_decoded.get("to_bow")
                    new_data["stern"] = message_decoded.get("to_stern")
                    new_data["port"] = message_decoded.get("to_port")
                    new_data["starboard"] = message_decoded.get("to_starboard")
                    new_data["destination"] = None
                    new_data["ais_type"] = message_decoded.get("type")
                    
                    db.ais_cyprus_static.insert_one(new_data)

                    message_json = json.dumps(message_decoded)
                    message_bytes = message_json.encode('utf-8')
                    kafka_producer_static.produce(message_bytes)
                    
               
                    

    except Exception as e:
        logging.error(f'UDP stream failure: {e}')

    

