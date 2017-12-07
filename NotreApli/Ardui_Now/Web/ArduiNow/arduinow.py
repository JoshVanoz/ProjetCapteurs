import os
import warnings
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)


from app import ArduiNow
from settings import DevConfig, ProdConfig

CONFIG = ProdConfig if os.environ.get('ENFERNO_ENV') == 'prod' else DevConfig

app = ArduiNow(CONFIG)


# app.run()
