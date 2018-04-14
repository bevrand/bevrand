from project.db import db_frontpage
from project.services.view_models import ErrorModel


def worker_for_frontpage_get(list_name):
    if list_name is None:
        front_page_list = db_frontpage.get_all_frontpage_lists()
        return_object = {'status_code': 200, 'body': front_page_list}
        return return_object
    else:
        list_name = list_name.lower()
        list_exists = db_frontpage.check_if_frontpage_list_exists(list_name)
        if list_exists:
            front_page_mongo = db_frontpage.get_frontpage_beverages(list_name)
            return_object = {'status_code': 200, 'body': front_page_mongo.__dict__}
            return return_object
        else:
            error_object = ErrorModel('frontpage', list_name, 'The frontpagelist you queried does not exist')
            return_object = {'status_code': 404, 'body': error_object}
            return return_object