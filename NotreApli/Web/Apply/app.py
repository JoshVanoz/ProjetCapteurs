from flask import Flask
from flask_script import Manager
import os.path
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
Bootstrap(app)

manager = Manager(app)

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))

app.config['SQLALCHEMY_DATABASE_URI']=(
    'sqlite:///'+mkpath('../tuto.db'))
db=SQLAlchemy(app)
