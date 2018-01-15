from datetime import datetime

class Mongoobject:
   'Common base class for all mongoobjects'

   def __init__(self, user, list, image_url=None):
      self.user = user
      self.list = list
      self.imageUrl = image_url
      self.dateinserted = datetime.utcnow()
      self.dateupdated = None
      self.beverages = []

class ReturnModelPost(object):
   def __init__(self, user_to_return, list_to_return, message, body):
      self.user = user_to_return
      self.list = list_to_return
      self.message = message
      self.newdata = body


class ReturnModelGet:

   def __init__(self, id, user_name, list_name, beverage_list, image_url=None):
      self.id = id
      self.user = user_name
      self.name = list_name
      self.imageUrl = image_url
      self.beverages = beverage_list