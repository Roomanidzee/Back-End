from flask import Flask
from flask.ext.session import Session

app = Flask(__name__)
app.config.from_object('app.config.BaseConfig')
app.secret_key = 'tb52h6b2oh56'
sess = Session()
sess.init_app(app)

from app import routes
