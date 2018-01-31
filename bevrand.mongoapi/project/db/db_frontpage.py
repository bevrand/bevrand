from werkzeug.local import LocalProxy

from project.db import db_connection
from project.api.models import ReturnModelGet

from flask import jsonify, g


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = db_connection.connect_to_mongo()
    return db


db = LocalProxy(get_db)


def get_frontpage_beverages(list):
    fpusers = db.frontpagestandard
    beverages = []
    specified_document = fpusers.find_one({'list': list})
    try:
        for drinks in specified_document['beverages']:
            beverages.append(drinks['name'])
    except:
        return "Unknown error"
    id = str(specified_document['_id'])
    user_name = 'frontPage'
    list_name = list
    image_url = specified_document['imagename']
    front_page_model = ReturnModelGet(id, user_name, list_name, beverages, image_url)
    return front_page_model


def check_if_frontpage_list_exists(list_name):
    fp_users = db.frontpagestandard
    specified_document = fp_users.find_one({'list': list_name})
    if specified_document is None:
        return False
    else:
        return True


def get_all_frontpage_lists():
    fp_users = db.frontpagestandard
    lists = []
    query = fp_users.find()
    if query.count() == 0:
        return 'Mongo query did not return any results'
    else:
        for result in query:
            lists.append(result['list'])
    set_list = set(lists)
    desc_list = list(set_list)
    return jsonify({'front_page_lists': desc_list})

