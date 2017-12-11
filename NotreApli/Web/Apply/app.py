from flask import Flask
from flask_script import Manager
import os.path

app = Flask(__name__)
app.debug = True

manager = Manager(app)
