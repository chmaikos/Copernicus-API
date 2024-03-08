import pymongo

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient["dock-mongo_mongodb_1"]

mycol = mydb["gap_events"]

gap_event = {
    "vessel_id": 000000000,
    "gap_start": 1689692459,
    "lon_start": 37.83,
    "lat_start": 37.83,
    "gap_end": 1689692469,
    "lon_end": 37.83,
    "lat_end": 37.84,
}

# spoofing_event = {
# 	"vessel_id": 235762000,
# 	"timestamp": 1689692459,
# 	"lon": 37.83,
# 	"lat": 37.83
# }

# area_event = {
# 	"vessel_id": 235762000,
# 	"timestamp": 1689692459,
# 	"lon": 37.83,
# 	"lat": 37.83,
# 	"area_id": 123456,
# 	"action": "enter/leave"
# }

# x = mycol.insert_one(gap_event)

# mylist = [
#   { "name": "Amy", "address": "Apple st 652"},
#   { "name": "Hannah", "address": "Mountain 21"},
#   { "name": "Michael", "address": "Valley 345"},
#   { "name": "Sandy", "address": "Ocean blvd 2"},
#   { "name": "Betty", "address": "Green Grass 1"},
#   { "name": "Richard", "address": "Sky st 331"},
#   { "name": "Susan", "address": "One way 98"},
#   { "name": "Vicky", "address": "Yellow Garden 2"},
#   { "name": "Ben", "address": "Park Lane 38"},
#   { "name": "William", "address": "Central st 954"},
#   { "name": "Chuck", "address": "Main Road 989"},
#   { "name": "Viola", "address": "Sideway 1633"}
# ]

# x = mycol.insert_many(mylist)

# collist = mydb.list_collection_names()
# if "gap_events" in collist:
#   print("The collection exists.")

myquery = {"vessel_id": 0}

for x in mycol.find(myquery):
    print(x)
