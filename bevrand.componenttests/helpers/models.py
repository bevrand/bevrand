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
    beverages: List[str]

    def __init__(self, display_name: str, image_url: str, beverages: List[str]):
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


class PlayListPostModel(PlaylistModel):

    username: str
    playlist: str

    def __init__(self, username: str, playlist: str, display_name: str, image_url: str, beverages: List[str]):
        super().__init__(display_name=display_name, image_url=image_url,
                         beverages=beverages)
        self.username = username
        self.playlist = playlist

    @staticmethod
    def from_dict(obj):
        beverages = obj.get("beverages")
        display_name = obj.get("displayName")
        image_url = obj.get("imageUrl")
        playlist = obj.get("list")
        user = obj.get("user")
        return PlayListPostModel(playlist=playlist, username=user, display_name=display_name,
                                 image_url=image_url, beverages=beverages)

    def to_dict(self):
        result: dict = {}
        result["beverages"] = self.beverages
        result["displayName"] = self.display_name
        result["imageUrl"] = self.image_url
        result["list"] = self.playlist
        result["user"] = self.username
        return result


class ProxyModel(PlayListPostModel):

    mongo_id: str
    iat: int
    jwtheader: Jwtheader
    jwttoken: str

    def __init__(self, mongo_id: str, playlist_post_model: PlayListPostModel, iat: int,
                 jwtheader: Jwtheader, jwttoken: str):
        super().__init__(username=playlist_post_model.username, playlist=playlist_post_model.playlist,
                         display_name=playlist_post_model.display_name, image_url=playlist_post_model.image_url,
                         beverages=playlist_post_model.beverages)
        self.mongo_id = mongo_id
        self.iat = iat
        self.jwtheader = jwtheader
        self.jwttoken = jwttoken

    @staticmethod
    def from_dict(obj):
        beverages = obj.get("beverages")
        display_name = obj.get("displayName")
        mongo_id = obj.get("id")
        image_url = obj.get("imageUrl")
        playlist = obj.get("list")
        user = obj.get("user")
        iat = obj.get("iat")
        jwtheader = Jwtheader.from_dict(obj.get("jwtheader"))
        jwttoken = obj.get("jwttoken")
        playlist_post_model = PlayListPostModel(username=user, playlist=playlist,
                                                display_name=display_name, image_url=image_url, beverages=beverages)
        return ProxyModel(mongo_id, playlist_post_model, iat, jwtheader, jwttoken)

    def to_dict(self):
        result: dict = {}
        result["beverages"] = self.beverages
        result["displayName"] = self.display_name
        result["id"] = self.mongo_id
        result["imageUrl"] = self.image_url
        result["list"] = self.playlist
        result["user"] = self.username
        result["iat"] = self.iat
        result["jwtheader"] = Jwtheader.to_dict(self.jwtheader)
        result["jwttoken"] = self.jwttoken
        return result
