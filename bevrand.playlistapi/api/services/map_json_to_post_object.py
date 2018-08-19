from datetime import datetime
from api.models.post_model import MongoObject


class ObjectMapper:

    def map_json_to_object(self, json_object, user_name, list_name=None):
        user = user_name.lower()
        if 'list' not in json_object:
            playlist_name = list_name.lower()
        else:
            playlist_name = json_object['list'].lower()
        beverages = []
        for bev in json_object['beverages']:
            tempjson = {"name": bev}
            beverages.append(tempjson)
        mongo_object = MongoObject(user, playlist_name, beverages)
        if 'imageUrl' not in json_object:
            mongo_object.imageUrl = "https://static.beveragerandomizer.com/file/beveragerandomizer/images/users/standardimage.png"
        else:
            mongo_object.imageUrl = json_object['imageUrl']
        if json_object['displayName'] is not None:
            mongo_object.displayName = json_object['displayName']
        mongo_object.dateinserted = datetime.utcnow().isoformat()
        mongo_object.dateupdated = datetime.utcnow().isoformat()
        return mongo_object