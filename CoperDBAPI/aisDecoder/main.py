from pyais.stream import UDPStream
import logging
import json

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

host = "0.0.0.0"
port = 9094

while True:
    try:
        for msg in UDPStream(host, port):
            message = msg.decode()

            if message is not None:
                message_json = message.to_json()
                logging.info(f'message: {message_json}')

                message_data = json.loads(message_json)
                message_type = message_data['decoded']['type']

                logging.info(f'message type: {message_type}')

                # Έλεγχος του τύπου του μηνύματος
                if message_type in [1, 2, 3, 18, 9]:
                    # Αποθήκευση στη συλλογή δυναμικών δεδομένων
                    db.ais_cyprus_dynamic.insert_one(message_data)
                    # Παραγωγή μηνύματος στο Kafka topic
                    kafka_producer.produce(json.dumps(message_data).encode('utf-8'))

                elif message_type in [4, 5, 24]:
                    # Αποθήκευση στη συλλογή στατικών δεδομένων
                    db.ais_cyprus_static.insert_one(message_data)
                    # Παραγωγή μηνύματος στο Kafka topic
                    kafka_producer.produce(json.dumps(message_data).encode('utf-8'))

                else:
                    # Αποθήκευση στη συλλογή other (χωρίς Kafka)
                    db.other.insert_one(message_data)

    except Exception as e:
        logging.error(f'UDP stream failure: {e}')

    

