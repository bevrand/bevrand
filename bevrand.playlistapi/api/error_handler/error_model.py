
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, meta=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.meta = meta
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['Error'] = self.message
        rv['Meta'] = self.meta
        return rv


