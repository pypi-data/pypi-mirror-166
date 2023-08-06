from lib2to3.pgen2.token import OP
import time
import os
import sys
import re
import random
import pandas
import flask

class OpenFlask:
    def __init__(self, app_name, flask_options, config_options={"SECRET_KEY": "s"}):
        #listofFlaskOpt = []
        #for flask_opt in flask_options:
            #listofFlaskOpt.append({flask_opt['name']: flask_opt['value']})

        self.app = flask.Flask(app_name, pandas.json_normalize(flask_options))
    
    def run(self, host='0.0.0.0', port=8080, debug=False):
        self.app.run()

app = OpenFlask('app', {}, {})
app.run()
