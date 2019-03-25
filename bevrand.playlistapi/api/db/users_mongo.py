from api.error_handler.error_model import InvalidUsage
from api.services.mapper import CursorMapper
from pymongo import errors


class UsersDb:

    #contructor
    def __init__(self, database):
        self.db = database.client.bevrand
        self.users = database.client.bevrand.users

    def get_all_user_lists(self, username):
        description_lists = []
        try:
            query = self.users.find({'user': username})
            mapper = CursorMapper()
            for result in query:
                res = mapper.map_cursor_to_object(result, username)
                description_lists.append(res)
            return description_lists
        except errors.ConnectionFailure:
            raise InvalidUsage('Could not connect to mongo', status_code=503)
        except errors.InvalidOperation:
            raise InvalidUsage('The mongo operation was not valid', status_code=400)

    def get_specific_list(self, user_name, list_name):
        specified_document = self.users.find_one({'user': user_name, 'list': list_name})
        if specified_document is None:
            raise InvalidUsage('List could not be found', status_code=404)
        users_model = CursorMapper.map_cursor_to_object(specified_document, user_name)
        return users_model

    def insert_new_list(self, post_data):
        try:
            self.users.insert_one(post_data)
        except errors.ConnectionFailure:
            raise InvalidUsage('Could not connect to mongo', status_code=503)
        except errors.OperationFailure:
            raise InvalidUsage('The insertion of a new list has failed', status_code=400)

    def delete_specific_list(self, to_remove_user, to_remove_list):
        try:
            self.users.delete_one({"user": to_remove_user, "list": to_remove_list})
            return
        except errors.ConnectionFailure:
            raise InvalidUsage('Could not connect to mongo', status_code=503)
        except errors.OperationFailure:
            raise InvalidUsage('Deletion of list has failed', status_code=400)

    def delete_all_user_lists(self, to_remove_user):
        try:
            self.users.delete_many({"user": to_remove_user})
            return
        except errors.ConnectionFailure:
            raise InvalidUsage('Could not connect to mongo', status_code=503)
        except errors.OperationFailure:
            raise InvalidUsage('Deletion of lists has failed', status_code=400)

    def update_specific_list(self, updated_object, old_user, old_list):
        specified_document = self.users.find_one({'user': old_user.lower(), 'list': old_list.lower()})
        id_to_be_used = specified_document['_id']
        updated_object = self.update_fields(specified_document, updated_object)
        try:
            result = self.users.update_one({'_id': id_to_be_used},
                                    {'$set':
                                        {"user": updated_object.username,
                                        "list": updated_object.playlist,
                                        "dateupdated": updated_object.date_updated,
                                        "beverages": updated_object.beverages,
                                        "imageUrl": updated_object.image_url,
                                        "displayName": updated_object.display_name
                                        }}, upsert=False)

            if result.modified_count == 1:
                return
            else:
                raise InvalidUsage('No list was updated', status_code=400)
        except errors.ConnectionFailure:
            raise InvalidUsage('Could not connect to mongo', status_code=503)
        except errors.OperationFailure:
            raise InvalidUsage('Update of list has failed', status_code=400)

    def check_if_user_exists(self, username):
        specified_document = self.users.find_one({'user': username})
        if specified_document is None:
            raise InvalidUsage('User could not be found', status_code=404)

    def check_if_userlist_exists(self, user_name, user_list):
        specified_document = self.users.find_one({'user': user_name.lower(), 'list': user_list.lower()})
        if specified_document is not None:
            raise InvalidUsage('User and list combination already exists', status_code=400)

    def check_if_userlist_can_be_found(self, user_name, user_list):
        specified_document = self.users.find_one({'user': user_name.lower(), 'list': user_list.lower()})
        if specified_document is None:
            raise InvalidUsage('List could not be found', status_code=404)

    def update_fields(self, old_document, new_document):
        if new_document.display_name is None or new_document.display_name.isspace() or new_document.display_name == "":
            new_document.display_name = old_document['displayName']
        if new_document.image_url is None or new_document.image_url.isspace() or new_document.image_url == "":
            new_document.image_url = old_document['imageUrl']
        return new_document
