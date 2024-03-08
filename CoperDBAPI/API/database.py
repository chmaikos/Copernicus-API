from config import Settings
from pykafka import KafkaClient
from pymongo import MongoClient

settings = Settings()

# MongoDB Connection
mongo_client = MongoClient(settings.MONGODB_URL)
db = mongo_client["kafka_db"]
ais_cyprus_dynamic_col = db["ais_cyprus_dynamic"]
ais_cyprus_static_col = db["ais_cyprus_static"]

# Kafka Connection
kafka_client = KafkaClient(hosts=settings.KAFKA_HOSTS)
kafka_producer_dynamic = kafka_client.topics[b"ais_cyprus_dynamic"].get_producer()
kafka_producer_static = kafka_client.topics[b"ais_cyprus_static"].get_producer()
