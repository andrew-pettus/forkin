from flask import Flask

app = Flask(__name__)

import os
try:
    env_level = os.getenv( "LOG_LEVEL", None )
    if env_level is None:
        app.logger.setLevel("ERROR")
    else:
        app.logger.setLevel(env_level)
except:
    app.logger.setLevel("ERROR")

from app import routes