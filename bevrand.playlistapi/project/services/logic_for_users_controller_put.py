from project.db import db_users
from project.services.custom_mapper import map_json_to_object
from project.services.view_models import ErrorModel, PostModelReturn


def worker_for_update(user_name, list_name, json_body):
    if user_name is not None and list_name is not None:
        user_name = user_name.lower()
        list_name = list_name.lower()

        user_exists = db_users.check_if_user_exists(user_name)
        if not user_exists:
            error_object = ErrorModel(user_name, list_name, 'The user you want to update does not exist')
            return_object = {'status_code': 404, 'body': error_object}
            return return_object

        list_exists = db_users.check_if_userlist_exists(user_name, list_name)
        if not list_exists:
            error_object = ErrorModel(user_name, list_name, 'The list you want to update does not exist')
            return_object = {'status_code': 404, 'body': error_object}
            return return_object

        mongo_object = map_json_to_object(json_body)
        if mongo_object.user == 'frontpage':
            error_object = ErrorModel(mongo_object.user, mongo_object.list,
                                      'frontpage is an invalid user - reserved')
            return_object = {'status_code': 403, 'body': error_object}
            return return_object
        if mongo_object.user != user_name:
            list_exists = db_users.check_if_userlist_exists(mongo_object.user, mongo_object.list)
            if list_exists:
                error_object = ErrorModel(mongo_object.user, mongo_object.list,
                                          'Unable to update this combination of list and user already exists')
                return_object = {'status_code': 400, 'body': error_object}
                return return_object

        updated_list = db_users.update_specific_list(mongo_object, user_name, list_name)
        put_model = PostModelReturn(user_name, list_name, updated_list, json_body)
        return_object = {'status_code': 200, 'body': put_model}
        return return_object