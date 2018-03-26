import redis


class BaseConfig(object):
    SECRET_KEY = 'secret_key'
    DEBUG = True
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis('192.168.99.100')
    API_URL = 'https://soul-cloud-api.herokuapp.com'
    UPLOAD_FOLDER = 'D:\\Projects\\Python\\SoulCloud\\backend_upload_folder'
    ALLOWED_EXTENSIONS = set(['.txt', '.json'])
