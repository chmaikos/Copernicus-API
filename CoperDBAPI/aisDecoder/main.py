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

data = len(list(UDPStream(host, port).read()))

logging.info(f'decoder:')
logging.info(f'decoder: {data}')
logging.info(f'decoder: {list(UDPStream(host, port).read())}')

for msg in UDPStream(host, port):
    message = msg.decode()
    logging.info(f'message: {message}')
