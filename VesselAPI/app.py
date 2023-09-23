from flask import Flask, Response, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
# from dotenv import load_dotenv

# load_dotenv()

app = Flask(__name__)
# mongo_db_url = os.environ.get("MONGO_DB_CONN_STRING")
# print(mongo_db_url)

client = MongoClient("mongodb://mongodb:27017")

db = client["dock-mongo_mongodb_1"]


# @app.route("/api/gaps", methods=['GET'])
# def get_gap_events():
#     # sensor_id = request.args.get('sensor_id')
#     # filter = {} if sensor_id is None else {"sensor_id": sensor_id}
#     gap_events = list(db.gap_events.find())
#     response = Response(response=dumps(gap_events), status=200,  mimetype="application/json")
#     return response

def init_steps():
    steps_per_alert_type = {
        "alert_id": 1,
        "description": "Suspicious/Unusual deviation from normalcy",
        "steps": [{
            "no": 1,
            "description": "Call the vessel",
            "status": "Not initialized"
        },
            {
                "no": 2,
                "description": "Inform the responsible authority",
                "status": "Not initialized"
            },
            {
                "no": 3,
                "description": "Deploy a UAV/EURMARS asset",
                "status": "Not initialized"
            },
            {
                "no": 4,
                "description": "Send naval responsible assets",
                "status": "Not initialized"
            }
        ]
    }
    collection = db["steps_per_threat"]
    collection.insert_one(steps_per_alert_type)


def init_recommended_steps():
    steps_per_alert_type = {
        "alert_id": 1,
        "description": "Suspicious/Unusual deviation from normalcy",
        "steps": [{
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
    collection = db["rec_steps_per_threat"]
    collection.insert_one(steps_per_alert_type)


# @app.route("/api/gaps/", methods=['GET'])
# def get_gap_events():
#     vessel_id = request.args.get('vessel_id')
#     start = request.args.get('start')
#     end = request.args.get('end')
#     filter = {}
#     if vessel_id is None:
#         if start != None and end != None:
#             start = int(start)
#             end = int(end)
#             app.logger.info("no vessel, both start end")
#             filter = { "gap_start": {"$gte": start}, "gap_end": {"$lte": end} }
#         if start != None and end is None:
#             start = int(start)
#             app.logger.info("no vessel, only start")
#             filter = { "gap_start": {"$gte": start} }
#         if start is None and end != None:
#             end = int(end)
#             app.logger.info("no vessel, only end")
#             filter = { "gap_end": {"$lte": end} }
#     else:
#         vessel_id = int(vessel_id)
#         if start != None and end != None:
#             app.logger.info("yes, both")
#             start = int(start)
#             end = int(end)
#             filter = { "vessel_id": vessel_id, "gap_start": {"$gte": start}, "gap_end": {"$lte": end} }
#         if start != None and end is None:
#             start = int(start)
#             app.logger.info("yes, only start")
#             filter = { "vessel_id": vessel_id, "gap_start": {"$gte": start} }
#         if start is None and end != None:
#             end = int(end)
#             app.logger.info("yes, only end")
#             filter = { "vessel_id": vessel_id, "gap_end": {"$lte": end} }
#     if not filter:
#         response = Response(response=dumps(list(filter)), status=200,  mimetype="application/json")
#     else:
#         gaps = list(db.gap_events.find(filter))
#         response = Response(response=dumps(gaps), status=200,  mimetype="application/json")
#     return response

# =========================== Manage COPS ===========================

@app.route("/api/alert-types/", methods=['GET'])
def get_alert_types():
    alert_types = db.alert_types.find({}, {"alert_type_id": 1, "description": 1})
    response = Response(response=dumps(alert_types), status=200, mimetype="application/json")
    return response


@app.route("/api/op-steps/", methods=['GET'])
def get_operational_steps():
    alert_type_id = request.args.get('alert_type_id')
    if alert_type_id != None:
        filter = {"alert_type_id": int(alert_type_id)}
        steps = list(db.alert_types.find(filter))
        response = Response(response=dumps(steps), status=200, mimetype="application/json")
        return response
    else:
        return "[]"


@app.route("/api/update-steps/", methods=['PUT'])
def update_steps():
    alert_type_id = request.args.get('alert_type_id')
    steps = request.get_json()
    filter = {"alert_type_id": int(alert_type_id)}
    update = {"$set": {"steps": steps}}
    db.alert_types.find_one_and_update(filter, update, upsert=False)
    resp = jsonify(success=True)
    return resp


# =========================== Alert Popup ===========================
# will need to initialize status when a new alert is generated

@app.route("/api/alert-steps/", methods=['GET'])
def get_operational_steps_per_alert():
    alert_id = request.args.get('alert_id')
    if alert_id != None:
        filter = {"alert_id": int(alert_id)}
        alert_type_id = db.alerts.find_one(filter, {"alert_type_id": 1})
        alert_type_id = alert_type_id["alert_type_id"]
        status = db.statuses.find({"alert_id": int(alert_id), "alert_type_id": alert_type_id})
        response = Response(response=dumps(status), status=200, mimetype="application/json")
        return response
    else:
        return "[]"


@app.route("/api/rec-steps/", methods=['GET'])
def get_recommended_steps():
    alert_id = request.args.get('alert_id')
    if alert_id != None:
        filter = {"alert_id": int(alert_id)}
        steps = list(db.alerts.find(filter))
        response = Response(response=dumps(steps), status=200, mimetype="application/json")
        return response
    else:
        return "[]"

@app.route('/status', methods=['GET'])
def get_status():

    api_is_up = True
    
    if api_is_up:
        response = {'status': 'success'}
    else:
        response = {'status': 'fail'}
    
    return jsonify(response)
# @app.route("/api/updatesteps/", methods=['PUT'])
# def update_steps():
#     alert_id = request.args.get('alert_id')
#     steps = request.get_json()
#     filter = { "alert_id": int(alert_id) }
#     update = {"$set":{"steps":steps}}
#     db.steps_per_threat.find_one_and_update(filter,update,upsert=False,return_document = ReturnDocument.AFTER)
#     resp = jsonify(success=True)
#     return resp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
