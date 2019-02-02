from typing import List


class PlaylistModel:

    username: str
    playlist: str
    display_name: str
    image_url: str
    beverages: List[str]

    def __init__(self, username: str, playlist: str, display_name: str, image_url: str, beverages: List[str]):
        self.username = username
        self.playlist = playlist
        self.display_name = display_name
        self.image_url = image_url
        self.beverages = beverages

    @staticmethod
    def from_dict(obj):
        playlist = obj.get("list")
        user = obj.get("user")
        display_name = obj.get("displayName")
        image_url = obj.get("imageUrl")
        beverages = obj.get("beverages")
        return PlaylistModel(username=user, playlist=playlist, display_name=display_name,
                             image_url=image_url, beverages=beverages)

    def to_dict(self):
        result = {}
        result["displayName"] = self.display_name
        result["imageUrl"] = self.image_url
        result["beverages"] = self.beverages
        result["list"] = self.playlist
        result["user"] = self.username
        return result


class PlayListViewModel(PlaylistModel):

    playlist_id: str

    def __init__(self, playlist_id: str, playlist_model: PlaylistModel):
        super().__init__(username=playlist_model.username, playlist=playlist_model.playlist,
                         display_name=playlist_model.display_name, image_url=playlist_model.image_url,
                         beverages=playlist_model.beverages)
        self.playlist_id = playlist_id

    @staticmethod
    def from_dict(obj):
        playlist_id = obj.get("_id")
        playlist = obj.get("list")
        user = obj.get("user")
        display_name = obj.get("displayName")
        image_url = obj.get("imageUrl")
        beverages = obj.get("beverages")
        playlist_model = PlaylistModel(username=user, playlist=playlist, display_name=display_name,
                                       image_url=image_url, beverages=beverages)
        return PlayListViewModel(playlist_id=playlist_id, playlist_model=playlist_model)

    def to_dict(self):
        result = {}
        result["id"] = self.playlist_id
        result["displayName"] = self.display_name
        result["imageUrl"] = self.image_url
        result["beverages"] = self.beverages
        result["list"] = self.playlist
        result["user"] = self.username
        return result


class PlayListPostModel(PlaylistModel):

    date_inserted = None
    date_updated = None

    def __init__(self, playlist_model: PlaylistModel, date_inserted, date_updated):
        super().__init__(username=playlist_model.username, playlist=playlist_model.playlist,
                         display_name=playlist_model.display_name, image_url=playlist_model.image_url,
                         beverages=playlist_model.beverages)
        self.date_inserted = date_inserted
        self.date_updated = date_updated

    @staticmethod
    def from_dict(obj):
        playlist = obj.get("list")
        user = obj.get("user")
        display_name = obj.get("displayName")
        image_url = obj.get("imageUrl")
        beverages = obj.get("beverages")
        date_inserted = obj.get("date_inserted")
        date_updated = obj.get("date_updated")
        playlist_model = PlaylistModel(username=user, playlist=playlist, display_name=display_name,
                                       image_url=image_url, beverages=beverages)
        return PlayListPostModel(playlist_model=playlist_model, date_inserted=date_inserted, date_updated=date_updated)

    def to_dict(self):
        result = {}
        result["displayName"] = self.display_name
        result["imageUrl"] = self.image_url
        result["beverages"] = self.beverages
        result["list"] = self.playlist
        result["user"] = self.username
        result["dateinserted"] = self.date_inserted
        result["dateupdated"] = self.date_updated
        return result
