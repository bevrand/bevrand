from datetime import datetime
from api.models.view_models import MongoObject


class ObjectMapper:

    def map_json_to_object(self, json_object):
        user = json_object['user'].lower()
        list = json_object['list'].lower()
        beverages = []
        for bev in json_object['beverages']:
            tempjson = {"name": bev}
            beverages.append(tempjson)
        mongo_object = MongoObject(user, list, beverages)
        if json_object['imageUrl'] is not None:
            mongo_object.imageUrl = json_object['imageUrl']
        if json_object['displayName'] is not None:
            mongo_object.displayName = json_object['displayName']
        mongo_object.dateinserted = datetime.utcnow().isoformat()
        mongo_object.dateupdated = datetime.utcnow().isoformat()
        return mongo_object