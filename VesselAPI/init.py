from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client["dock-mongo_mongodb_1"]


def init_alert_types():
    alert_types = [{
        "alert_type_id": 1,
        "description": "Suspicious activity",
        "steps": [{
            "no": 1,
            "description": "Call the vessel",
        },
            {
                "no": 2,
                "description": "Inform the responsible authority",
            },
            {
                "no": 3,
                "description": "Deploy a UAV/EURMARS asset",
            },
            {
                "no": 4,
                "description": "Send naval responsible assets",
            }
        ]
    },
        {
            "alert_type_id": 2,
            "description": "Unusual deviation from normalcy",
            "steps": [
                {
                    "no": 1,
                    "description": "Call the vessel",
                },
                {
                    "no": 2,
                    "description": "Inform the responsible authority",
                },
                {
                    "no": 3,
                    "description": "Send naval responsible assets",
                }]
        }]
    collection = db["alert_types"]
    collection.insert_many(alert_types)


def init_alerts():
    alerts = [{
        "alert_id": 1,
        "alert_type_id": 1,
        "description": "Suspicious/Unusual deviation from normalcy",
        "rec_steps": [
            {
                "no": 1,
                "description": "Call the vessel",
            },
            {
                "no": 2,
                "description": "Inform the responsible authority",
            }]
    }]
    collection = db["alerts"]
    collection.insert_many(alerts)


def init_status():
    status = {
        "alert_id": 1,
        "alert_type_id": 1,
        "steps": [
            {
                "no": 1,
                "description": "Call the vessel",
                "status": "Not initialized"
            },
            {
                "no": 2,
                "description": "Inform the responsible authority",
                "status": "Not initialized"
            }
        ]
    }
    collection = db["statuses"]
    collection.insert_one(status)


if __name__ == '__main__':
    init_alert_types()
    init_alerts()
    init_status()
