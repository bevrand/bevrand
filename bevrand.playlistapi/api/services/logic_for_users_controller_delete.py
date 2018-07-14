from api.db import db_users
from api.services.view_models import ErrorModel


def worker_for_delete(user_name, list_name):
    if user_name is not None and list_name is None:
        user_name = user_name.lower()
        user_exists = db_users.check_if_user_exists(user_name)
        if not user_exists:
            error_object = ErrorModel(user_name, list_name, 'The user you want to delete does not exist')
            return_object = {'status_code': 404, 'body': error_object}
            return return_object
        deleted_user = db_users.delete_specific_user(user_name)
        dict_to_return = {user_name: deleted_user}
        return_object = {'status_code': 200, 'body': dict_to_return}
        return return_object

    if user_name is not None and list_name is not None:
        user_name = user_name.lower()
        list_name = list_name.lower()

        user_exists = db_users.check_if_user_exists(user_name)
        if not user_exists:
            error_object = ErrorModel(user_name, list_name, 'The user you want to delete does not exist')
            return_object = {'status_code': 404, 'body': error_object}
            return return_object

        list_exists = db_users.check_if_userlist_exists(user_name, list_name)
        if not list_exists:
            error_object = ErrorModel(user_name, list_name, 'The list you want to delete does not exist')
            return_object = {'status_code': 404, 'body': error_object}
            return return_object

        deleted_list = db_users.delete_specific_list(user_name, list_name)
        dict_to_return = {user_name + " " + list_name: deleted_list}
        return_object = {'status_code': 200, 'body': dict_to_return}
        return return_object