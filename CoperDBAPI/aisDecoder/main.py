from pyais.stream import UDPStream
import logging

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

try:
    # Continue with the rest of your code...
    for msg in UDPStream(host, port):
    
        message = msg.decode()
        logging.info(f'message: {message}')
except Exception as e:
    logging.error(f'UDP stream failure: {e}')
    

