import threading
import time

from ais_decode import start_udp_listener
from fastapi import FastAPI
from producers.wave import process_and_publish_wave_data
from routers import (
    ais_cyprus_dynamic_router,
    ais_cyprus_static_router,
    data_router,
    lab_router,
    living_lab_router,
    weather_router,
)

app = FastAPI(title="Copernicus API", version="0.0.1beta")

app.include_router(lab_router, prefix="/api", tags=["lab"])
app.include_router(living_lab_router, prefix="/api", tags=["living_lab"])
app.include_router(data_router, prefix="/api", tags=["data"])
app.include_router(
    ais_cyprus_dynamic_router, prefix="/api", tags=["ais_cyprus_dynamic"]
)
app.include_router(ais_cyprus_static_router, prefix="/api", tags=["ais_cyprus_static"])
app.include_router(weather_router, prefix="/api", tags=["weather"])


@app.on_event("startup")
def run_background_tasks():
    time.sleep(3600)
    # Starting the UDP listener in its own thread
    udp_listener_thread = threading.Thread(target=start_udp_listener, daemon=True)
    udp_listener_thread.start()

    # Starting the wave data processor in its own thread
    wave_processor_thread = threading.Thread(
        target=process_and_publish_wave_data, daemon=True
    )
    wave_processor_thread.start()
