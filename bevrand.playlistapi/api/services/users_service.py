import api
from api.db.users_mongo import UsersDb


class UsersService:

    def retrieve_all_lists_for_user(self, user_name):
        mongo_users = UsersDb(api.mongo.db)
        mongo_result = mongo_users.get_all_user_lists(user_name.lower())
        user_lists = {"result": mongo_result}
        return user_lists