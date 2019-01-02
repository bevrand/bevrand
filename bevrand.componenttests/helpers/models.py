from helpers.random_name_generator import HelperClass

class AuthenticationModel:

    id: str
    username: str
    email_address: str
    valid: bool
    password: str

    def __init__(self, id: str, username: str, email_address: str, valid: bool, password: str):
        self.id = id
        self.username = username
        self.email_address = email_address
        self.valid = valid
        self.password = password

    @staticmethod
    def from_dict(obj):
        id = obj.get("id")
        username = obj.get("username")
        email_address = obj.get("emailAddress")
        valid = obj.get("valid")
        password = obj.get("password")
        return AuthenticationModel(id, username, email_address, valid, password)

    def to_dict(self):
        result = {}
        result["id"] = self.id
        result["username"] = self.username
        result["email_address"] = self.email_address
        result["valid"] = self.valid
        result["password"] = self.password
        return result

class PlaylistModel:

    display_name: str
    image_url: str
    beverages: list

    def __init__(self, display_name: str, image_url: str, beverages: list):
        self.display_name = display_name
        self.image_url = image_url
        self.beverages = beverages

    @staticmethod
    def from_dict(obj):
        display_name = obj.get("displayName")
        image_url = obj.get("imageUrl")
        beverages = obj.get("beverages")
        return PlaylistModel(display_name, image_url, beverages)

    @staticmethod
    def create_random_playlist():
        result = {}
        result["displayName"] = HelperClass.random_word_letters_only(15)
        result["imageUrl"] = "http://www.testimage.com/image.png"
        beverages = []
        for x in range(0, 4):
            beverage = HelperClass.random_word_letters_only(5)
            beverages.append(beverage)
        result["beverages"] = beverages
        return result

    def to_dict(self):
        result = {}
        result["displayName"] = self.display_name
        result["imageUrl"] = self.image_url
        result["beverages"] = self.beverages
        return result

