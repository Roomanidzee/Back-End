import os

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', '346b2h456b48rgbr')
    SESSION_TYPE = 'redis'
    SESSION_REDIS = '192.168.99.100:6379'
    API_URL = 'https://soul-cloud-api.herokuapp.com'