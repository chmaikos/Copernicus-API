#!/bin/bash

KAFKA_HOST=kafka
KAFKA_PORT=29092

echo "Waiting for Kafka to be ready..."
until nc -z $KAFKA_HOST $KAFKA_PORT; do
  echo "Kafka is unavailable - sleeping"
  sleep 10
done

echo "Kafka is up - executing command"
exec "$@"
