from datetime import datetime

class Mongoobject:
   'Common base class for all mongoobjects'

   def __init__(self, user, list):
      self.user = user
      self.list = list
      self.dateinserted = datetime.utcnow()
      self.dateupdated = None
      self.beverages = []

class ReturnModel(object):
   def __init__(self, user_to_return, list_to_return, message, body):
      self.user = user_to_return
      self.list = list_to_return
      self.message = message
      self.newdata = body