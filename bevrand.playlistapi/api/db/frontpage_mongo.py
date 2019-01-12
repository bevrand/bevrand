from api.services.map_cursor_to_dict import CursorMapper
from api.error_handler.error_model import InvalidUsage
from pymongo import errors


class FrontPageDb:

    #constructor
    def __init__(self, database):
        self.db = database.client.bevrand
        self.frontpage = database.client.bevrand.frontpagestandard

    def get_frontpage_beverages(self, list_name):
        try:
            specified_document = self.frontpage.find_one({'list': list_name})
            if specified_document is None:
                raise InvalidUsage('List could not be found', status_code=404)
            mapper = CursorMapper()
            front_page_model = mapper.map_cursor_to_object(specified_document, 'frontpage')
            return front_page_model
        except errors.ConnectionFailure:
            raise InvalidUsage('Could not connect to mongo', status_code=503)
        except errors.InvalidOperation:
            raise InvalidUsage('The mongo operation was not valid', status_code=400)

    def retrieve_all_frontpage_lists(self):
        users = []
        query = self.frontpage.find()
        mapper = CursorMapper()
        for result in query:
            res = mapper.map_cursor_to_object(result, 'frontpage')
            users.append(res.__dict__)
        return users


