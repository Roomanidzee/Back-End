from flask import Flask
from flask.ext.session import Session

app = Flask(__name__)
app.config.from_object('app.config.BaseConfig')
sess = Session()
sess.init_app(app)

from app.routes import book_routes, user_routes, like_routes
