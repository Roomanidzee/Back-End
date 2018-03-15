from flask import Flask
from flask.ext.session import Session

app = Flask(__name__)
app.config.from_pyfile('the_config.cfg')
sess = Session(app)

from app import routes
