from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://mongodb:27017"
    KAFKA_HOSTS: str = "kafka1:29092"
    UDP_LISTEN_HOST: str = "0.0.0.0"
    UDP_LISTEN_PORT: int = 9094
    USERNAME: str = "mmini1"
    PASSWORD: str = "Artemis2000"
    PROD_WAVE_OUTPUT_FILENAME: str = "data/CMEMS_Wave3H.nc"
    WAVE_TOPIC: str = "wave_topic"
    KAFKA_PRODUCER_CONFIG: dict = {"bootstrap.servers": "kafka1:29092"}
    DEFAULT_LONGITUDE: float = 27.917171
    DEFAULT_LATITUDE: float = 43.173814
    DEFAULT_RADIUS: int = 20

    class Config:
        env_file = ".env"


settings = Settings()
