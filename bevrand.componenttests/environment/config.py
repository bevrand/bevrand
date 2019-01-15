class BaseConfig:
    """Base configuration"""
    DEBUG = True
    TESTING = True


class Local(BaseConfig):
    """Local configuration"""
    authentication_url = "http://localhost:4570/api"
    playlist_url = "http://localhost:4550/api/v1"
    randomize_url = "http://localhost:4560/api"
    proxy_url = "http://localhost:4540/api"
    highscore_url = "http://localhost:4580/api/v1/highscores/"


class Test(BaseConfig):
    """Docker configuration"""
    authentication_url = "http://authenticationapi:5000/api"
    playlist_url = "http://playlistapi:5000/api/v1"
    randomize_url = "http://randomizerapi:5000/api"
    proxy_url = "http://proxyapi:5000/api"
    highscore_url = "http://highscoreapi:5000/api/v1/highscores/"
