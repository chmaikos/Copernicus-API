import threading

import config
from ais_decode import start_udp_listener
from database import db_vessel
from fastapi import FastAPI
from producers.wave import process_and_publish_wave_data
from producers.wind import process_and_publish_wind_data
from routers import ais_router, data_router, lab_router, vessel_router

app = FastAPI(title="Copernicus API", version="0.0.1beta")
app.include_router(lab_router, prefix="/api", tags=["Lab API"])
app.include_router(data_router, prefix="/api", tags=["Copernicus API"])
app.include_router(ais_router, prefix="/api", tags=["AIS API"])
app.include_router(vessel_router, prefix="/api", tags=["Vessel API"])


@app.on_event("startup")
def run_background_tasks():
    config.init_alerts(db_vessel)
    config.init_COPs(db_vessel)
    # Starting the UDP listener in its own thread
    udp_listener_thread = threading.Thread(target=start_udp_listener, daemon=True)
    udp_listener_thread.start()

    # Starting the wave data processor in its own thread
    wave_processor_thread = threading.Thread(
        target=process_and_publish_wave_data, daemon=True
    )
    wave_processor_thread.start()

    # Starting the wind data processor in its own thread
    wind_processor_thread = threading.Thread(
        target=process_and_publish_wind_data, daemon=True
    )
    wind_processor_thread.start()
