class MongoObject:
    # Common base class for all mongo objects

    def __init__(self, user_name, list_name, beverages, display_name=None, image_url=None):
        self.user = user_name
        self.list = list_name
        self.beverages = beverages
        self.displayName = display_name
        self.imageUrl = image_url
        self.dateinserted = None
        self.dateupdated = None



class ErrorModel():

    def __init__(self, user_to_return, list_to_return, message):
        self.user = user_to_return
        self.list = list_to_return
        self.message = message


class SuccessModel():
    def __init__(self, user_to_return, list_to_return, message):
        self.user = user_to_return
        self.list = list_to_return
        self.message = message


class PostModelReturn(SuccessModel):

    def __init__(self, user_to_return, list_to_return, message, body):
        SuccessModel.__init__(self, user_to_return, list_to_return, message)
        self.body = body


class PutModelReturn(SuccessModel):

    def __init__(self, user_to_return, list_to_return, message, body):
        SuccessModel.__init__(self, user_to_return, list_to_return, message)
        self.body = body