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

host = "host.docker.internal"
port = 9094

logging.info(f'decoder:')

for msg in UDPStream(host, port):
    message = msg.decode()
    logging.info(f'message: {message}')
