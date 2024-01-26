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
            
                message = message.to_json()
                
                logging.info(f'message: {message}')
                
                # Έλεγχος του τύπου του μηνύματος
                if 'type' in message and message['type'] in [1, 2, 3]:
                    # Αποθήκευση στη συλλογή δυναμικών δεδομένων
                    logging.info(f'123')
                else:
                    # Αποθήκευση στη συλλογή στατικών δεδομένων
                    logging.info(f'4')
    
    except Exception as e:
        logging.error(f'UDP stream failure: {e}')

    

