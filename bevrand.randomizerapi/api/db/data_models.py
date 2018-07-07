class ErrorModel():

    def __init__(self, valid, message, status_code):
        self.valid = valid
        self.message = message
        self.status_code = status_code


class SuccessModel():

    def __init__(self, valid):
        self.valid = valid


class SuccessModelRedis(SuccessModel):

    def __init__(self, valid, sorted_list):
        SuccessModel.__init__(self, valid)
        self.sorted_list = sorted_list