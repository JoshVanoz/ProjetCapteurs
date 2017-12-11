from flask import Flask
from flask_script import Manager
import os.path
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.debug = True
Bootstrap(app)

manager = Manager(app)
app.debug = True

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
