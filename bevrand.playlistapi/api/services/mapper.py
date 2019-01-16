from datetime import datetime
from api.models.database_models import PlaylistModel, PlayListPostModel, PlayListViewModel


class ObjectMapper:

    @staticmethod
    def map_json_to_object(json_object, user_name, list_name=None):
        json_object['user'] = user_name.lower()
        if 'list' not in json_object:
            json_object['list'] = list_name.lower()
        else:
            json_object['list'] = json_object['list'].lower()
        beverages = []
        for bev in json_object['beverages']:
            tempjson = {"name": bev}
            beverages.append(tempjson)
        json_object['beverages'] = beverages
        post_model = PlaylistModel.from_dict(json_object)

        if post_model.image_url is None:
            post_model.imageUrl = \
                "https://static.beveragerandomizer.com/file/beveragerandomizer/images/users/standardimage.png"

        date_to_insert = datetime.utcnow().isoformat()
        mongo_post_model = PlayListPostModel(playlist_model=post_model, date_inserted=date_to_insert,
                                             date_updated=date_to_insert)
        return mongo_post_model


class CursorMapper:

    @staticmethod
    def map_cursor_to_object(specified_document, username):
        beverages = []
        for drinks in specified_document['beverages']:
            beverages.append(drinks['name'])
        specified_document['beverages'] = beverages
        mongo_id = str(specified_document['_id'])
        mongo_model = PlaylistModel.from_dict(specified_document)
        mongo_model.username = username

        front_page_model = PlayListViewModel(playlist_id=mongo_id, playlist_model=mongo_model)
        front_page_model = front_page_model.to_dict()
        return front_page_model
