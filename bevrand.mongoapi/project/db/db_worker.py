from werkzeug.local import LocalProxy
import json

from project.api.models import Mongoobject
from project.db import db_connection, error_handler

from flask import jsonify, g
from datetime import datetime


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = db_connection.connect_to_mongo()
    return db


db = LocalProxy(get_db)


#db = Database.get_db()


def get_all_users():
    user = db.users
    users = []
    query = user.find()
    if query.count() == 0:
        raise error_handler.InvalidUsage('Mongoquery invalid no results', status_code=410)
    else:
        for user in query:
            users.append(user['user'])
    setlist = set(users)
    desclist = list(setlist)
    return jsonify({'users': desclist})


def get_all_descriptions(username):
    description_list = db.users
    description_lists = []
    query = description_list.find({'user' : username})
    if query.count() != 0:
        for desclist in query:
            description_lists.append(desclist['list'])
    else:
        raise error_handler.InvalidUsage('Not a valid user, nothing to show', status_code=410)
    return jsonify({'descriptions': description_lists})


def get_specific_drinklist(username, desclist):
    user = db.users
    beverages = []
    specified_document = user.find_one({'user': username, 'list': desclist})
    if specified_document is not None:
        for drinks in specified_document['beverages']:
            beverages.append(drinks['name'])
    else:
        raise error_handler.InvalidUsage('Mongoquery invalid no results', status_code=410)
    return jsonify({'beverages': beverages})


def insert_new_list(requestjson, usertoinsert, list):
    user = db.users
    toinsert = Mongoobject(usertoinsert, list)
    toinsert.dateupdated = datetime.utcnow().isoformat()
    toinsert.dateinserted = datetime.utcnow().isoformat()
    for bev in requestjson['beverages']:
        tempjson = {"name": bev}
        toinsert.beverages.append(tempjson)
    postdata = toinsert.__dict__
    insertid = user.insert_one(postdata).inserted_id
    if insertid is not None:
        return "Your list with id: {0} has been inserted".format(insertid)
    else:
        return error_handler.InvalidUsage('Insert not successful, please make sure to post valid json', status_code=410)

def check_if_user_exists(username):
    user = db.users
    specified_document = user.find_one({'user': username})
    if specified_document is None:
        return False
    else:
        return True


def check_if_userlist_already_exists(username, userlist):
    user = db.users
    specified_document = user.find_one({'user': username, 'list': userlist})
    if specified_document is None:
        return False
    else:
        return True


def delete_specific_list(to_remove_user, to_remove_list):
    user = db.users
    try:
        delete_res = user.delete_one({"user": to_remove_user, "list": to_remove_list})
        if delete_res.deleted_count == 1:
            return "Delete of {0} mongoobject(s) was successful".format(delete_res.deleted_count)
        else:
            return error_handler.InvalidUsage('Your delete is not valid make sure to use: user and list as a json', status_code=410)
    except:
        return error_handler.InvalidUsage('Your delete is not valid make sure to use: user and list as a json', status_code=410)


def update_specific_list(requestjson, old_user, old_list):
    user = db.users
    specifieddocument = user.find_one({'user': old_user, 'list': old_list})
    idtobeused = specifieddocument['_id']
    toupdate = Mongoobject(user=requestjson['user'], list=requestjson['list'])
    toupdate.dateupdated = datetime.utcnow().isoformat()
    for bev in requestjson['beverages']:
        tempjson = {"name": bev}
        toupdate.beverages.append(tempjson)
    try:
        result = user.update_one({'_id' : idtobeused},
                                   {'$set' :
                                        { "user": toupdate.user,
                                          "list" : toupdate.list,
                                          "dateupdated" : toupdate.dateupdated,
                                          "beverages" : toupdate.beverages
                                          }}, upsert=False)

        if result.modified_count == 1:
            return "Update successful for mongoid: {0}".format(idtobeused)
    except:
        raise error_handler.InvalidUsage('Update not succesful please be put valid json', status_code=410)
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
