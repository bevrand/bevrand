from datetime import datetime


class MongoObject:
    # Common base class for all mongo objects

    def __init__(self, user_name, list_name, image_url=None):
        self.user = user_name
        self.list = list_name
        self.imageUrl = image_url
        self.dateinserted = datetime.utcnow()
        self.dateupdated = None
        self.beverages = []


class ReturnModel(object):

    def __init__(self, user_to_return, list_to_return, message):
        self.user = user_to_return
        self.list = list_to_return
        self.message = message


class ReturnModelGet():

    def __init__(self, id_name, user_name, list_name, beverage_list, image_url=None):
        self.id = id_name
        self.user = user_name
        self.name = list_name
        self.imageUrl = image_url
        self.beverages = beverage_list


class ReturnModelPut(ReturnModel):

    def __init__(self, user_to_return, list_to_return, message, body):
        ReturnModel.__init__(self, user_to_return, list_to_return, message)
        self.body = body


class ReturnModelPost(ReturnModel):

    def __init__(self, user_to_return, list_to_return, message, body):
        ReturnModel.__init__(self, user_to_return, list_to_return, message)
        self.body = body
