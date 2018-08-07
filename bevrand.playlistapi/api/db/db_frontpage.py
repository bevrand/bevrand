from ..db.database_models import MongoObject
from api import MONGO as mongo


def get_frontpage_beverages(list):
    fpusers = mongo.db.frontpagestandard
    specified_document = fpusers.find_one({'list': list})
    front_page_model = map_cursor_to_object(specified_document)
    return front_page_model


def check_if_frontpage_list_exists(list_name):
    fp_users = mongo.db.frontpagestandard
    specified_document = fp_users.find_one({'list': list_name})
    if specified_document is None:
        return False
    else:
        return True


def get_all_frontpage_lists():
    fp_users = mongo.db.frontpagestandard
    users = []
    query = fp_users.find()
    if query.count() == 0:
        return 'Mongo query did not return any results'
    else:
        for result in query:
            res = map_cursor_to_object(result)
            users.append(res.__dict__)
    return users


def map_cursor_to_object(specified_document):
    id = str(specified_document['_id'])
    user_name = 'frontpage'
    list_name = specified_document['list']
    beverages = []
    for drinks in specified_document['beverages']:
        beverages.append(drinks['name'])
    display_name = specified_document['displayName']
    image_url = specified_document['imageUrl']
    front_page_model = MongoObject(id, user_name, list_name, beverages, display_name, image_url)
    front_page_model.dateinserted = str(specified_document['dateinserted'])
    front_page_model.dateupdated = str(specified_document['dateupdated'])
    return front_page_model