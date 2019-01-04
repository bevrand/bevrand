from helpers.random_name_generator import HelperClass
from typing import List

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

class Jwtheader(object):

    alg: str
    type: str

    def __init__(self, alg: str, type: str):
        self.alg = alg
        self.type = type

    @staticmethod
    def from_dict(obj):
        alg = obj.get("alg")
        type = obj.get("type")
        return Jwtheader(alg, type)

    def to_dict(self):
        result = {}
        result["alg"] = self.alg
        result["type"] = self.type
        return result

class ProxyModel:
    beverages: List[str]
    display_name: str
    id: str
    image_url: str
    list: str
    user: str
    iat: int
    jwtheader: Jwtheader
    jwttoken: str

    def __init__(self, beverages: List[str], display_name: str, id: str, image_url: str, list: str, user: str, iat: int, jwtheader: Jwtheader, jwttoken: str):
        self.beverages = beverages
        self.display_name = display_name
        self.id = id
        self.image_url = image_url
        self.list = list
        self.user = user
        self.iat = iat
        self.jwtheader = jwtheader
        self.jwttoken = jwttoken

    @staticmethod
    def from_dict(obj):
        beverages = obj.get("beverages")
        display_name = obj.get("displayName")
        id = obj.get("id")
        image_url = obj.get("imageUrl")
        list = obj.get("list")
        user = obj.get("user")
        iat = obj.get("iat")
        jwtheader = Jwtheader.from_dict(obj.get("jwtheader"))
        jwttoken = obj.get("jwttoken")
        return ProxyModel(beverages, display_name, id, image_url, list, user, iat, jwtheader, jwttoken)

    def to_dict(self):
        result: dict = {}
        result["beverages"] = self.beverages
        result["displayName"] = self.display_name
        result["id"] = self.id
        result["imageUrl"] = self.image_url
        result["list"] = self.list
        result["user"] = self.user
        result["iat"] = self.iat
        result["jwtheader"] = Jwtheader.to_dict(self.jwtheader)
        result["jwttoken"] = self.jwttoken
        return result
