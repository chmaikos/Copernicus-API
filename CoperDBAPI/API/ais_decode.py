import json
from datetime import datetime

from config import settings
from database import db
from pyais.stream import UDPStream


def start_udp_listener():
    while True:
        try:
            for msg in UDPStream(settings.UDP_LISTEN_HOST, settings.UDP_LISTEN_PORT):
                message = msg.decode()

                if message is not None:
                    message_json = message.to_json()
                    message_data = json.loads(message_json)
                    message_type = message_data["decoded"]["type"]
                    message_decoded = message_data["decoded"]

                    current_utc_time = datetime.utcnow()
                    formatted_time = current_utc_time.strftime("%Y-%m-%d %H:%M:%S")
                    new_data = {
                        "timestamp": formatted_time,
                        "mmsi": message_decoded.get("mmsi"),
                        "longitude": message_decoded.get("lon"),
                        "latitude": message_decoded.get("lat"),
                        "heading": message_decoded.get("heading"),
                        "sog": message_decoded.get("speed"),
                        "cog": message_decoded.get("course"),
                        "ais_type": message_decoded.get("type"),
                    }

                    if message_type in [1, 2, 3, 9, 18]:  # Dynamic data types
                        if "nav_status" in message_decoded:
                            new_data["nav_status"] = message_decoded["nav_status"]
                        db.ais_cyprus_dynamic.insert_one(new_data)

                    elif message_type == 5 or (
                        message_type == 24 and "to_port" in message_decoded
                    ):
                        additional_fields = [
                            "imo",
                            "ship_name",
                            "call_sign",
                            "ship_type",
                            "draught",
                            "bow",
                            "stern",
                            "port",
                            "starboard",
                            "destination",
                        ]
                        for field in additional_fields:
                            if field in message_decoded:
                                new_data[field] = message_decoded[field]
                        db.ais_cyprus_static.insert_one(new_data)

        except Exception as e:
            print(f"UDP stream failure: {e}")
