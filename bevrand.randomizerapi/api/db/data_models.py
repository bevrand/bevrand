class ErrorModel():

    def __init__(self, valid, message, status_code):
        self.valid = valid
        self.message = message
        self.status_code = status_code


class SuccessModelRedis():

    def __init__(self, sorted_list):
        self.sorted_list = sorted_list