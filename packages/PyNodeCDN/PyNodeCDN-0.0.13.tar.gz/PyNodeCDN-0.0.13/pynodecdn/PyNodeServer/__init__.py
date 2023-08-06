import time
import os
import sys
import re
import random
import pandas
from flask import Flask

class OpenFlask:
    def __init__(self, app_name, flask_options, config_options={"SECRET_KEY": "s"}):
        #listofFlaskOpt = []
        #for flask_opt in flask_options:
            #listofFlaskOpt.append({flask_opt['name']: flask_opt['value']})

        self.app = Flask(app_name, pandas.json_normalize(flask_options))
