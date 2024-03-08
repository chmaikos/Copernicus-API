import json

from bson.json_util import dumps
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://mongodb:27017")

db = client["dock-mongo_mongodb_1"]

# =========================== Manage COPS ===========================


@app.route("/api/threats/", methods=["GET"])
def get_cops():
    cops = db["COPs"].find({}, {"id": 1, "threat_name": 1})
    response = Response(response=dumps(cops), status=200, mimetype="application/json")
    return response


@app.route("/api/threat-cops/", methods=["GET"])
def get_cops_for_threat():
    id = request.args.get("id")
    filter = {"id": id}
    cops = list(db["COPs"].find(filter))[0]
    response = Response(response=dumps(cops), status=200, mimetype="application/json")
    return response


@app.route("/api/update-cops/", methods=["PUT"])
def update_steps():
    id = request.args.get("id")
    json_request = request.get_json()
    steps = json_request["steps"]
    threat_description = json_request["threat_description"]
    print(threat_description)
    filter = {"id": id}
    update = {"$set": {"threat_description": threat_description, "steps": steps}}
    db["COPs"].find_one_and_update(filter, update, upsert=False)
    resp = jsonify(success=True)
    return resp


# =========================== DSS ===========================
# msg_id refers to specific alerts while id of COPS refers to the id of the threat types.


@app.route("/api/rops/", methods=["GET"])
def get_rops():
    msg_id = request.args.get("msg_id")
    filter = {"msg_id": msg_id}
    rops = db["alerts"].find(filter)
    json_resp = dumps(rops)
    data = json.loads(json_resp)
    steps_set = set()
    rec_steps_set = set()
    # find the remaining steps
    for i in data[0]["steps"]:
        desc = i["description"]
        steps_set.add(desc)
    for i in data[0]["rec_steps"]:
        desc = i["description"]
        rec_steps_set.add(desc)
    diff = list(steps_set.difference(rec_steps_set))
    data[0]["other_steps"] = diff
    response = Response(
        response=dumps(list(data)[0]), status=200, mimetype="application/json"
    )
    return response


# updates status and recommended steps
@app.route("/api/update-status-and-rops/", methods=["PUT"])
def update_rops():
    msg_id = request.args.get("msg_id")
    json_request = request.get_json()
    steps = json_request["steps"]
    rec_steps = json_request["rec_steps"]
    filter = {"msg_id": msg_id}
    update = {"$set": {"steps": steps, "rec_steps": rec_steps}}
    db["alerts"].find_one_and_update(filter, update, upsert=False)
    resp = jsonify(success=True)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
