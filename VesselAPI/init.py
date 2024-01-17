from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient("mongodb://mongodb:27017")
db = client["dock-mongo_mongodb_1"]


def init_COPs():
    COPS = [
		{
			"msg ID": "1",
			"message type": "COP",
			"threat name": "Sudden change in SOG",
			"threat description": "Sudden change in SOG",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "2",
			"message type": "COP",
			"threat name": "Abrupt change in COG",
			"threat description": "Abrupt change in COG",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "3",
			"message type": "COP",
			"threat name": "Suspicious anchoring",
			"threat description": "Suspicious anchoring",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "4",
			"message type": "COP",
			"threat name": "Dark vessel detected in a predefined area of interest",
			"threat description": "Dark vessel detected in a predefined area of interest",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "5",
			"message type": "COP",
			"threat name": "Detected a vessel that shut down its AIS transmission",
			"threat description": "Detected a vessel that shut down its AIS transmission",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "6",
			"message type": "COP",
			"threat name": "Detect a rendezvous of two or more vessels",
			"threat description": "Detect a rendezvous of two or more vessels",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "7",
			"message type": "COP",
			"threat name": "Identify suspicious anomalies in different weather, tidal and seasonal conditions",
			"threat description": "Identify suspicious anomalies in different weather, tidal and seasonal conditions",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "8",
			"message type": "COP",
			"threat name": "Detected a vessel approaching the shoreline",
			"threat description": "Detected a vessel approaching the shoreline",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "9",
			"message type": "COP",
			"threat name": "Detected people on the deck",
			"threat description": "Detected people on the deck",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "10",
			"message type": "COP",
			"threat name": "Track people coming ashore from the vessel",
			"threat description": "Track people coming ashore from the vessel",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "11",
			"message type": "COP",
			"threat name": "Detect change in navigational status",
			"threat description": "Detect change in navigational status",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Inform the responsible authority"
				},
				{
					"no": 3,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 4,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"msg ID": "12",
			"message type": "COP",
			"threat name": "Detect dark vessel in a predefined area",
			"threat description": "Detect dark vessel in a predefined area",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"msg ID": "13",
			"message type": "COP",
			"threat name": "Check if AIS required",
			"threat description": "Check if AIS required",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"msg ID": "14",
			"message type": "COP",
			"threat name": "AIS spoofing detected",
			"threat description": "AIS spoofing detected",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"msg ID": "15",
			"message type": "COP",
			"threat name": "Detect vessel entering/leaving area shutting down its AIS",
			"threat description": "Detect vessel entering/leaving area shutting down its AIS",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"msg ID": "16",
			"message type": "COP",
			"threat name": "Detect vessel in distress",
			"threat description": "Detect vessel in distress",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Inform the responsible authority"
				},
				{
					"no": 3,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 4,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"msg ID": "17",
			"message type": "COP",
			"threat name": "Detected xx number of people on a vessel or by the shore, or…?",
			"threat description": "Detected xx number of people on a vessel or by the shore, or…?",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "18",
			"message type": "COP",
			"threat name": "Detect oil spill in predefined area",
			"threat description": "Detect oil spill in predefined area",
			"steps": [
				{
					"no": 1,
					"description": "Call the responsible authority"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"msg ID": "19",
			"message type": "COP",
			"threat name": "Detect if a vessel is on a collision course with another or with coast",
			"threat description": "Detect if a vessel is on a collision course with another or with coast",
			"steps": [
				{
					"no": 1,
					"description": "Inform the proper authorities (MRCC)"
				}
			]
		},
		{
			"msg ID": "20",
			"message type": "COP",
			"threat name": "Track Detected people coming ashore from the vessel",
			"threat description": "Track Detected people coming ashore from the vessel",
			"steps": [
				{
					"no": 1,
					"description": "Interception on land and sea"
				}
			]
		},
		{
			"msg ID": "21",
			"message type": "COP",
			"threat name": "Track if the group of people landed from the vessel is divided into two or more groups",
			"threat description": "Track if the group of people landed from the vessel is divided into two or more groups",
			"steps": [
				{
					"no": 1,
					"description": "Interception on land and sea"
				}
			]
		},
		{
			"msg ID": "22",
			"message type": "COP",
			"threat name": "Detected people walking on foot picked up by a vehicle",
			"threat description": "Detected people walking on foot picked up by a vehicle",
			"steps": [
				{
					"no": 1,
					"description": "Interception on land"
				}
			]
		}
	]
    collection = db["COPs"]
    collection.insert_many(COPS)

def init_alerts():
	alerts = [
		{
			"msg ID": "1",
			"message type": "alert",
			"threat name": "Sudden change in SOG",
			"threat description": "Sudden change in SOG",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "2",
			"message type": "alert",
			"threat name": "Abrupt change in COG",
			"threat description": "Abrupt change in COG",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "3",
			"message type": "alert",
			"threat name": "Suspicious anchoring",
			"threat description": "Suspicious anchoring",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "4",
			"message type": "alert",
			"threat name": "Dark vessel detected in a predefined area of interest",
			"threat description": "Dark vessel detected in a predefined area of interest",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "5",
			"message type": "alert",
			"threat name": "Detected a vessel that shut down its AIS transmission",
			"threat description": "Detected a vessel that shut down its AIS transmission",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "6",
			"message type": "alert",
			"threat name": "Detect a rendezvous of two or more vessels",
			"threat description": "Detect a rendezvous of two or more vessels",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "7",
			"message type": "alert",
			"threat name": "Identify suspicious anomalies in different weather, tidal and seasonal conditions",
			"threat description": "Identify suspicious anomalies in different weather, tidal and seasonal conditions",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "8",
			"message type": "alert",
			"threat name": "Detected a vessel approaching the shoreline",
			"threat description": "Detected a vessel approaching the shoreline",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "9",
			"message type": "alert",
			"threat name": "Detected people on the deck",
			"threat description": "Detected people on the deck",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "10",
			"message type": "alert",
			"threat name": "Track people coming ashore from the vessel",
			"threat description": "Track people coming ashore from the vessel",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "11",
			"message type": "alert",
			"threat name": "Detect change in navigational status",
			"threat description": "Detect change in navigational status",
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
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"msg ID": "12",
			"message type": "alert",
			"threat name": "Detect dark vessel in a predefined area",
			"threat description": "Detect dark vessel in a predefined area",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"msg ID": "13",
			"message type": "alert",
			"threat name": "Check if AIS required",
			"threat description": "Check if AIS required",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"msg ID": "14",
			"message type": "alert",
			"threat name": "AIS spoofing detected",
			"threat description": "AIS spoofing detected",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"msg ID": "15",
			"message type": "alert",
			"threat name": "Detect vessel entering/leaving area shutting down its AIS",
			"threat description": "Detect vessel entering/leaving area shutting down its AIS",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"msg ID": "16",
			"message type": "alert",
			"threat name": "Detect vessel in distress",
			"threat description": "Detect vessel in distress",
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
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"msg ID": "17",
			"message type": "alert",
			"threat name": "Detected xx number of people on a vessel or by the shore, or…?",
			"threat description": "Detected xx number of people on a vessel or by the shore, or…?",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"msg ID": "18",
			"message type": "alert",
			"threat name": "Detect oil spill in predefined area",
			"threat description": "Detect oil spill in predefined area",
			"steps": [
				{
					"no": 1,
					"description": "Call the responsible authority",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the responsible authority"
				}
			]
		},
		{
			"msg ID": "19",
			"message type": "alert",
			"threat name": "Detect if a vessel is on a collision course with another or with coast",
			"threat description": "Detect if a vessel is on a collision course with another or with coast",
			"steps": [
				{
					"no": 1,
					"description": "Inform the proper authorities (MRCC)",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Inform the proper authorities (MRCC)"
				}
			]
		},
		{
			"msg ID": "20",
			"message type": "alert",
			"threat name": "Track Detected people coming ashore from the vessel",
			"threat description": "Track Detected people coming ashore from the vessel",
			"steps": [
				{
					"no": 1,
					"description": "Interception on land and sea",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Interception on land and sea"
				}
			]
		},
		{
			"msg ID": "21",
			"message type": "alert",
			"threat name": "Track if the group of people landed from the vessel is divided into two or more groups",
			"threat description": "Track if the group of people landed from the vessel is divided into two or more groups",
			"steps": [
				{
					"no": 1,
					"description": "Interception on land and sea",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Interception on land and sea"
				}
			]
		},
		{
			"msg ID": "22",
			"message type": "alert",
			"threat name": "Detected people walking on foot picked up by a vehicle",
			"threat description": "Detected people walking on foot picked up by a vehicle",
			"steps": [
				{
					"no": 1,
					"description": "Interception on land",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Interception on land"
				}
			]
		}
	]
	collection = db["alerts"]
	collection.insert_many(alerts)

    
if __name__ == '__main__':
	cops = db["COPs"]
	cops.drop()
	alerts = db["alerts"]
	alerts.drop()
	init_COPs()
	init_alerts()
