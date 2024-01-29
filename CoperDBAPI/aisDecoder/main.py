from pyais.stream import UDPStream
import logging
import json
import pymongo
from pykafka import KafkaClient

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

                logging.info(f'message: {message_data['decoded']}')

                # Έλεγχος του τύπου του μηνύματος
                if message_type in [1, 2, 3, 18, 9]:
                    # Αποθήκευση στη συλλογή δυναμικών δεδομένων
                    db.ais_cyprus_dynamic.insert_one(message_data['decoded'])
                    # Παραγωγή μηνύματος στο Kafka topic
                    #kafka_producer_dynamic.produce(json.dumps(message_data['decoded']).encode('utf-8'))

                elif message_type in [4, 5, 24]:
                    # Αποθήκευση στη συλλογή στατικών δεδομένων
                    db.ais_cyprus_static.insert_one(message_data['decoded'])
                    # Παραγωγή μηνύματος στο Kafka topic
                    #kafka_producer_static.produce(json.dumps(message_data['decoded']).encode('utf-8'))

                else:
                    # Αποθήκευση στη συλλογή other (χωρίς Kafka)
                    db.other.insert_one(message_data['decoded'])

    except Exception as e:
        logging.error(f'UDP stream failure: {e}')

    

