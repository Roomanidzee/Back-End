from flask import Flask
from flask_session import Session
import os

app_settings = os.getenv('app.config.BaseConfig')

app = Flask(__name__)
app.config.from_object(app_settings)
sess = Session()
sess.init_app(app)

from app import routes
