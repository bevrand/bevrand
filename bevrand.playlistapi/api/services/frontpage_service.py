import api
from api.db.frontpage_mongo import FrontPageDb


class FrontPageService:

    def retrieve_front_page_list(self, list_name):
        mongo_front_page = FrontPageDb(api.mongo.db)
        return mongo_front_page.get_frontpage_beverages(list_name.lower())

    def retrieve_all_front_page_lists(self):
        mongo_front_page = FrontPageDb(api.mongo.db)
        return mongo_front_page.retrieve_all_frontpage_lists()
