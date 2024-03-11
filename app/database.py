import motor.motor_asyncio
from config import Settings
from pykafka import KafkaClient

settings = Settings()

# MongoDB Connection using Motor for async operations
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = mongo_client["kafka_db"]
db_vessel = mongo_client["VesselAPI"]
ais_cyprus_dynamic_col = db["ais_cyprus_dynamic"]
ais_cyprus_static_col = db["ais_cyprus_static"]

# Kafka Connection
kafka_client = KafkaClient(hosts=settings.KAFKA_HOSTS)
kafka_producer_dynamic = kafka_client.topics[b"ais_cyprus_dynamic"].get_producer()
kafka_producer_static = kafka_client.topics[b"ais_cyprus_static"].get_producer()
