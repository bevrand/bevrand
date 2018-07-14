from datetime import datetime

from api.services.view_models import MongoObject


def map_json_to_object(json):
    user = json['user'].lower()
    list = json['list'].lower()
    beverages = []
    for bev in json['beverages']:
        tempjson = {"name": bev}
        beverages.append(tempjson)
    mongo_object = MongoObject(user, list, beverages)
    if json['imageUrl'] is not None:
        mongo_object.imageUrl = json['imageUrl']
    if json['displayName'] is not None:
        mongo_object.displayName = json['displayName']
    mongo_object.dateinserted = datetime.utcnow().isoformat()
    mongo_object.dateupdated = datetime.utcnow().isoformat()
    return mongo_object