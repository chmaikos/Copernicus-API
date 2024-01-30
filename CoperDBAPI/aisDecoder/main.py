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
mycol_other = db["ais_cyprus_other"]

mycol_static.drop()
mycol_dynamic.drop()
mycol_other.drop()

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
                new_data = {}
                if message_type in [1, 2, 3]:
                    
                    new_data["timestamp"] = message_decoded.get("second")
                    new_data["navStatus"] = message_decoded.get("old_field1")
                    new_data["lon"] = message_decoded.get("lon")
                    new_data["lat"] = message_decoded.get("lat")
                    new_data["heading"] = message_decoded.get("heading")
                    new_data["sog"] = message_decoded.get("speed")
                    new_data["cog"] = message_decoded.get("course")

                    db.ais_cyprus_dynamic.insert_one(new_data)
                    kafka_producer_dynamic.produce(new_data)
                    
                elif message_type is [9, 18]:
            
                    new_data["timestamp"] = message_decoded.get("second")
                    new_data["navStatus"] = -1
                    new_data["lon"] = message_decoded.get("lon")
                    new_data["lat"] = message_decoded.get("lat")
                    new_data["heading"] = message_decoded.get("heading")
                    new_data["sog"] = message_decoded.get("speed")
                    new_data["cog"] = message_decoded.get("course")
    
                    db.ais_cyprus_dynamic.insert_one(new_data)
                    kafka_producer_dynamic.produce(new_data)

                elif message_type is 5:

                    day = message_decoded.get("day")
                    hour = message_decoded.get("hour")
                    minute = message_decoded.get("minute")
                    month = message_decoded.get("month")

                    timestamp = datetime(month=month, day=day, hour=hour, minute=minute)
                    timestamp = timestamp.timestamp()
                    
                    new_data["timestamp"] = timestamp
                    new_data["imo"] = message_decoded.get("imo")
                    new_data["shipname"] = message_decoded.get("shipname")
                    new_data["callsign"] = message_decoded.get("callsign")
                    new_data["shipType"] = message_decoded.get("shiptype")
                    new_data["draught"] = message_decoded.get("draught")
                    new_data["bow"] = message_decoded.get("to_bow")
                    new_data["stern"] = message_decoded.get("to_stern")
                    new_data["port"] = message_decoded.get("to_port")
                    new_data["starboard"] = message_decoded.get("to_starboard")
                    new_data["destination"] = message_decoded.get("destination")

                    db.ais_cyprus_static.insert_one(new_data)
                    kafka_producer_static.produce(new_data)

                elif message_type is 24 and message_decoded.get("to_port") is not None:

                    logging.info(f'message: {message_data}')

                    # day = message_decoded.get("day")
                    # second = message_decoded.get("hour")
                    # minute = message_decoded.get("minute")
                    # month = message_decoded.get("month")
                    new_data["timestamp"] = -1
                    new_data["imo"] = -1
                    new_data["shipname"] = ''
                    new_data["callsign"] = message_decoded.get("callsign")
                    new_data["shipType"] = message_decoded.get("shiptype")
                    new_data["draught"] = -1
                    new_data["bow"] = message_decoded.get("to_bow")
                    new_data["stern"] = message_decoded.get("to_stern")
                    new_data["port"] = message_decoded.get("to_port")
                    new_data["starboard"] = message_decoded.get("to_starboard")
                    new_data["destination"] = ''
                    
                    db.ais_cyprus_static.insert_one(new_data)
                    kafka_producer_static.produce(new_data)
                    
               
                    

    except Exception as e:
        logging.error(f'UDP stream failure: {e}')

    

