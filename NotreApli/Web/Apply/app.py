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
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

app.config['SECRET_KEY']="f80e3c9d-4229-4e14-a302-7b624a52f6eb"
from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"
