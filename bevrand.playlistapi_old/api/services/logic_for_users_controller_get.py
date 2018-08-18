from api.db import db_users
from api.services.view_models import ErrorModel


def worker_for_users_get(user_name, list_name):
    if list_name is not None and user_name is None:
        error_object = ErrorModel(user_name, list_name, 'You can not query lists without supplying a user')
        return_object = {'status_code': 400, 'body': error_object}
        return return_object

    if user_name is not None and list_name is not None:
        user_name = user_name.lower()
        list_name = list_name.lower()

        user_exists = db_users.check_if_user_exists(user_name)
        if not user_exists:
            error_object = ErrorModel(user_name, list_name, 'The user you queried does not exist')
            return_object = {'status_code': 404, 'body': error_object}
            return return_object

        list_exists = db_users.check_if_userlist_exists(user_name, list_name)
        if not list_exists:
            error_object = ErrorModel(user_name, list_name, 'The list you queried does not exist')
            return_object = {'status_code': 404, 'body': error_object}
            return return_object

        user_list = db_users.get_specific_list(user_name, list_name)
        return_object = {'status_code': 200, 'body': user_list.__dict__}
        return return_object
    else:
        error_object = ErrorModel(user_name, list_name, 'You seem to be entering null values')
        return_object = {'status_code': 404, 'body': error_object}
        return return_object


def worker_for_all_users():
    all_users = db_users.get_all_users()
    dict_to_return = {'Active Users': all_users}
    return_object = {'status_code': 200, 'body': dict_to_return}
    return return_object


def worker_for_all_lists_of_a_specific_user(user_name):
    user_name = user_name.lower()
    user_exists = db_users.check_if_user_exists(user_name)
    if not user_exists:
        error_object = ErrorModel(user_name, "Unknown", 'The user you queried does not exist')
        return_object = {'status_code': 404, 'body': error_object}
        return return_object

    user_lists = db_users.get_all_descriptions(user_name)
    dict_to_return = {"lists": user_lists}
    return_object = {'status_code': 200, 'body': dict_to_return}
    return return_object