from flask import Flask, Response, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)


client = MongoClient("mongodb://mongodb:27017")

db = client["dock-mongo_mongodb_1"]


def init_steps():
    steps_per_alert_type = {
        "alert_id": 1,
        "description": "Suspicious/Unusual deviation from normalcy",
        "steps": [
            {"no": 1, "description": "Call the vessel", "status": "Not initialized"},
            {
                "no": 2,
                "description": "Inform the responsible authority",
                "status": "Not initialized",
            },
            {
                "no": 3,
                "description": "Deploy a UAV/EURMARS asset",
                "status": "Not initialized",
            },
            {
                "no": 4,
                "description": "Send naval responsible assets",
                "status": "Not initialized",
            },
        ],
    }
    collection = db["steps_per_threat"]
    collection.insert_one(steps_per_alert_type)


def init_recommended_steps():
    steps_per_alert_type = {
        "alert_id": 1,
        "description": "Suspicious/Unusual deviation from normalcy",
        "steps": [
            {"no": 1, "description": "Call the vessel", "status": "Not initialized"},
            {
                "no": 2,
                "description": "Inform the responsible authority",
                "status": "Not initialized",
            },
        ],
    }
    collection = db["rec_steps_per_threat"]
    collection.insert_one(steps_per_alert_type)


@app.route("/api/alert-types/", methods=["GET"])
def get_alert_types():
    alert_types = db.alert_types.find({},
                                      {"alert_type_id": 1, "description": 1})
    response = Response(
        response=dumps(alert_types), status=200, mimetype="application/json"
    )
    return response


@app.route("/api/op-steps/", methods=["GET"])
def get_operational_steps():
    alert_type_id = request.args.get("alert_type_id")
    if alert_type_id is not None:
        filter = {"alert_type_id": int(alert_type_id)}
        steps = list(db.alert_types.find(filter))
        response = Response(
            response=dumps(steps), status=200, mimetype="application/json"
        )
        return response
    else:
        return "[]"


@app.route("/api/update-steps/", methods=["PUT"])
def update_steps():
    alert_type_id = request.args.get("alert_type_id")
    steps = request.get_json()
    filter = {"alert_type_id": int(alert_type_id)}
    update = {"$set": {"steps": steps}}
    db.alert_types.find_one_and_update(filter, update, upsert=False)
    resp = jsonify(success=True)
    return resp


# =========================== Alert Popup ===========================
# will need to initialize status when a new alert is generated


@app.route("/api/alert-steps/", methods=["GET"])
def get_operational_steps_per_alert():
    alert_id = request.args.get("alert_id")
    if alert_id is not None:
        filter = {"alert_id": int(alert_id)}
        alert_type_id = db.alerts.find_one(filter, {"alert_type_id": 1})
        alert_type_id = alert_type_id["alert_type_id"]
        status = db.statuses.find(
            {"alert_id": int(alert_id), "alert_type_id": alert_type_id}
        )
        response = Response(
            response=dumps(status), status=200, mimetype="application/json"
        )
        return response
    else:
        return "[]"


@app.route("/api/rec-steps/", methods=["GET"])
def get_recommended_steps():
    alert_id = request.args.get("alert_id")
    if alert_id is not None:
        filter = {"alert_id": int(alert_id)}
        steps = list(db.alerts.find(filter))
        response = Response(
            response=dumps(steps), status=200, mimetype="application/json"
        )
        return response
    else:
        return "[]"


@app.route("/status", methods=["GET"])
def get_status():
    api_is_up = True

    if api_is_up:
        response = {"status": "success"}
    else:
        response = {"status": "fail"}

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
