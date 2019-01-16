from ..models.view_models import MongoObject


class CursorMapper:

    def map_cursor_to_object(self, specified_document, username):
        id = str(specified_document['_id'])
        user_name = username
        list_name = specified_document['list']
        beverages = []
        for drinks in specified_document['beverages']:
            beverages.append(drinks['name'])
        display_name = specified_document['displayName']
        image_url = specified_document['imageUrl']
        front_page_model = MongoObject(id, user_name, list_name, beverages, display_name, image_url)
        return front_page_model
