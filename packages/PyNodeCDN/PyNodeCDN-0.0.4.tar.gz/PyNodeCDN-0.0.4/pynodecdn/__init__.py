import requests
import random
import os
import sys
import re
import time
import json

class Flask():
    def __init__(self, app):
        self.app = app
        self.route = '/nodecdn.js'

        @app.route(self.route)
        def nodecdnpath():
            return "Works!"
        
    def change_path(self, path):
        self.route = path