import redis


class BaseConfig(object):
    SECRET_KEY = 'secret_key'
    FLASK_DEBUG = 1
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis('192.168.99.100')
    API_URL = 'https://soul-cloud-api.herokuapp.com'
    UPLOAD_FOLDER = 'D:\\Projects\\Python\\SoulCloud\\site_backend\\app\\backend_files'
    ALLOWED_EXTENSIONS = {'.txt', '.json'}
