class MongoObject:
    # Common base class for all mongo objects

    def __init__(self, id, user_name, list_name, beverages, display_name=None, image_url=None):
        self.id = id
        self.user = user_name
        self.list = list_name
        self.displayName = display_name
        self.imageUrl = image_url
        self.dateinserted = None
        self.dateupdated = None
        self.beverages = beverages