class Proxy:
    login = '/authentication-api/login'
    register = '/authentication-api/register'
    highscore = '/highscore-api/v1/highscore'
    ocr = '/ocr-api/v1/base64'
    playlist_public = '/playlist-api/v2/frontpage'
    playlist_private = '/playlist-api/v1/private'
    randomize = '/randomize-api/v2/randomize'
    recommendation = '/recommendation-api/v1'


class BaseConfig:
    """Base configuration"""
    DEBUG = True
    TESTING = True


class Local(BaseConfig):
    """Local configuration"""
    authentication_url = "http://localhost:4570/api"
    playlist_url = "http://localhost:4550/api/v1"
    ocr_url = "http://localhost:4600/api/v1"
    randomize_url = "http://localhost:4560/api"
    proxy_url = "http://localhost:4540"
    proxy_endpoints = Proxy()
    highscore_url = "http://localhost:4580/api/v1/highscores/"
    recommendation_url = "http://localhost:4590/api/v1/"


class Test(BaseConfig):
    """Docker configuration"""
    authentication_url = "http://authenticationapi:5000/api"
    playlist_url = "http://playlistapi:5000/api/v1"
    ocr_url = "http://ocrapi:5000/api/v1"
    randomize_url = "http://randomizerapi:5000/api"
    proxy_url = "http://proxyapi:5000"
    proxy_endpoints = Proxy()
    highscore_url = "http://highscoreapi:5000/api/v1/highscores/"
    recommendation_url = "http://recommendationapi:5000/api/v1/"
