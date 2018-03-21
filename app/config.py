import redis

class BaseConfig(object):
    DEBUG = True
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis('192.168.99.100')
    API_URL = 'https://soul-cloud-api.herokuapp.com'