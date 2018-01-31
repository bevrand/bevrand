from werkzeug.local import LocalProxy
import json

from project.api.models import MongoObject
from project.db import db_connection

from flask import jsonify, g
from datetime import datetime


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = db_connection.connect_to_mongo()
    return db


db = LocalProxy(get_db)


# db = Database.get_db()


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


def get_all_descriptions(username):
    description_list = db.users
    description_lists = []
    query = description_list.find({'user': username})
    if query.count() != 0:
        for desc_list in query:
            description_lists.append(desc_list['list'])
    else:
        return 'Not a valid user, nothing to show'
    return description_lists


def get_specific_drinklist(username, desclist):
    user = db.users
    beverages = []
    specified_document = user.find_one({'user': username, 'list': desclist})
    if specified_document is not None:
        for drinks in specified_document['beverages']:
            beverages.append(drinks['name'])
    else:
        return 'Mongo query did not return any results'
    return beverages


def insert_new_list(request_json, user_to_insert, list_name):
    user = db.users
    to_insert = MongoObject(user_to_insert, list_name)
    to_insert.dateupdated = datetime.utcnow().isoformat()
    to_insert.dateinserted = datetime.utcnow().isoformat()
    for bev in request_json['beverages']:
        tempjson = {"name": bev}
        to_insert.beverages.append(tempjson)
    post_data = to_insert.__dict__
    insert_id = user.insert_one(post_data).inserted_id
    if insert_id is not None:
        return "Your list with id: {0} has been inserted".format(insert_id)
    else:
        return 'Insert not successful, please make sure to post valid json'


def delete_specific_list(to_remove_user, to_remove_list):
    user = db.users
    try:
        delete_res = user.delete_one({"user": to_remove_user, "list": to_remove_list})
        if delete_res.deleted_count == 1:
            return "Delete of {0} mongoobject(s) was successful".format(delete_res.deleted_count)
        else:
            return 'Your delete is not valid make sure to use: user and list as a json'
    except:
        return 'Your delete is not valid make sure to use: user and list as a json'


def update_specific_list(request_json, old_user, old_list):
    user = db.users
    specified_document = user.find_one({'user': old_user, 'list': old_list})
    id_to_be_used = specified_document['_id']
    to_update = MongoObject(user_name=request_json['user'].lower(), list_name=request_json['list'].lower())
    to_update.dateupdated = datetime.utcnow().isoformat()
    for bev in request_json['beverages']:
        tempjson = {"name": bev}
        to_update.beverages.append(tempjson)
    try:
        result = user.update_one({'_id': id_to_be_used},
                                 {'$set':
                                      {"user": to_update.user,
                                       "list": to_update.list,
                                       "dateupdated": to_update.dateupdated,
                                       "beverages": to_update.beverages
                                       }}, upsert=False)

        if result.modified_count == 1:
            return "Update successful for mongoid: {0}".format(id_to_be_used)
    except:
        return 'Update not successful please be put valid json'


def check_if_user_exists(username):
    user = db.users
    specified_document = user.find_one({'user': username})
    if specified_document is None:
        return False
    else:
        return True


def check_if_userlist_exists(user_name, user_list):
    user = db.users
    specified_document = user.find_one({'user': user_name, 'list': user_list})
    if specified_document is None:
        return False
    else:
        return True


'''
def get_all_beverages():
    users = mongo.db.users
    beverages = []
    query = users.find()
    if query.count() != 0:
        for drink in query:
            for drinks in drink['beverages']:
                beverages.append(drinks['name'])
    else:
        raise InvalidUsage('Mongoquery invalid no results', status_code=410)
    return jsonify({'beverages': beverages})
'''
