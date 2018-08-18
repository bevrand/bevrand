from api.db import db_users
from api.services.custom_mapper import map_json_to_object
from api.services.view_models import ErrorModel, PostModelReturn


def worker_for_post(posted_user):
    mongo_object = map_json_to_object(posted_user)
    if mongo_object.user == 'frontpage':
        error_object = ErrorModel(mongo_object.user, mongo_object.list, 'frontpage is an invalid user - reserved')
        return_object = { 'status_code': 403, 'body': error_object}
        return return_object
    list_exists = db_users.check_if_userlist_exists(mongo_object.user, mongo_object.list)
    if list_exists:
        error_object = ErrorModel(mongo_object.user, mongo_object.list, 'Unable to insert list already exists')
        return_object = {'status_code': 400, 'body': error_object}
        return return_object
    insert_list_res = db_users.insert_new_list(mongo_object)
    post_model = PostModelReturn(mongo_object.user, mongo_object.list, insert_list_res, posted_user)
    return_object = {'status_code': 200, 'body': post_model}
    return return_object