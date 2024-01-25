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

host = "127.0.0.1"
port = 9094

logging.info(f'decoder:')

# Initialize data outside the try block
data = None

# Try to read data
try:
    data = len(list(UDPStream(host, port).read()))
except Exception as e:
    logging.exception(f'An error occurred: {e}')

logging.info(f'decoder: {data}')

# Check if data is available before logging
if data is not None:
    logging.info(f'decoder: {data}')
    logging.info(f'decoder: {list(UDPStream(host, port).read())}')

# Continue with the rest of your code...
for msg in UDPStream(host, port):
    message = msg.decode()
    logging.info(f'message: {message}')
