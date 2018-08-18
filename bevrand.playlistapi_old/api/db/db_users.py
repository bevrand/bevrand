from werkzeug.local import LocalProxy
import json

from ..db.database_models import MongoObject
from api.db import db_connection

from flask import jsonify, g
from datetime import datetime


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = db_connection.connect_to_mongo()
    return db


db = LocalProxy(get_db)


def get_all_users():
    user = db.users
    users = []
    query = user.find()
    if query.count() == 0:
        return 'Mongo query did not return any results'
    else:
        for user in query:
            users.append(user['user'])
    setlist = set(users)
    desc_list = list(setlist)
    return desc_list


def get_all_descriptions(user_name):
    description_list = db.users
    description_lists = []
    query = description_list.find({'user': user_name})
    if query.count() != 0:
        for desc_list in query:
            description_lists.append(desc_list['list'])
    return description_lists


def get_specific_list(user_name, list_name):
    user = db.users
    specified_document = user.find_one({'user': user_name, 'list': list_name})
    users_model = map_cursor_to_object(specified_document)
    return users_model


def insert_new_list(mongo_object):
    user = db.users
    post_data = mongo_object.__dict__
    insert_id = user.insert_one(post_data).inserted_id
    if insert_id is not None:
        return "Your list with id: {0} has been inserted".format(insert_id)
    else:
        return 'Insert not successful, please make sure to post valid json'


def delete_specific_list(to_remove_user, to_remove_list):
    user = db.users
    delete_res = user.delete_one({"user": to_remove_user, "list": to_remove_list})
    if delete_res.deleted_count == 1:
        return "Delete of {0} mongoobject(s) was successful".format(delete_res.deleted_count)
    else:
        return 'Your delete is not valid make sure to use: user and list as a json'


def delete_specific_user(to_remove_user):
    user = db.users
    delete_res = user.delete_many({"user": to_remove_user})
    return "Delete of {0} mongoobject(s) was successful".format(delete_res.deleted_count)


def update_specific_list(updated_object, old_user, old_list):
    user = db.users
    specified_document = user.find_one({'user': old_user, 'list': old_list})
    id_to_be_used = specified_document['_id']
    updated_object = update_fields(specified_document, updated_object)
    try:
        result = user.update_one({'_id': id_to_be_used},
                                 {'$set':
                                      {"user": updated_object.user,
                                       "list": updated_object.list,
                                       "dateupdated": updated_object.dateupdated,
                                       "beverages": updated_object.beverages,
                                       "imageUrl": updated_object.imageUrl,
                                       "displayName": updated_object.displayName
                                       }}, upsert=False)

        if result.modified_count == 1:
            return "Update successful for mongoid: {0}".format(id_to_be_used)
    except:
        return 'Update not successful please put valid json'


def check_if_user_exists(username):
    user = db.users
    specified_document = user.find_one({'user': username})
    if specified_document is None:
        return False
    else:
        return True


def check_if_userlist_exists(user_name, user_list):
    user = db.users
    specified_document = user.find_one({'user': user_name.lower(), 'list': user_list.lower()})
    if specified_document is None:
        return False
    else:
        return True


def map_cursor_to_object(specified_document):
    id = str(specified_document['_id'])
    user_name = specified_document['user']
    list_name = specified_document['list']
    beverages = []
    for drinks in specified_document['beverages']:
        beverages.append(drinks['name'])
    display_name = specified_document['displayName']
    image_url = specified_document['imageUrl']
    users_model = MongoObject(id, user_name, list_name, beverages, display_name, image_url)
    users_model.dateinserted = specified_document['dateinserted']
    users_model.dateupdated = specified_document['dateupdated']
    return users_model


def update_fields(old_document, new_document):
    if new_document.displayName is None or new_document.displayName.isspace() or new_document.displayName == "":
        new_document.displayName = old_document['displayName']
    if new_document.imageUrl is None or new_document.imageUrl.isspace() or new_document.imageUrl == "":
        new_document.imageUrl = old_document['imageUrl']
    return new_document
