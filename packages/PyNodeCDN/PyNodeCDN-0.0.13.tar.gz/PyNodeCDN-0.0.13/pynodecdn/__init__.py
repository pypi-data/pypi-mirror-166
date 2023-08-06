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
        
    def change_path(self, path):
        self.route = path
        Flask.apply(self)

    def apply(self):
    # A system function for applying changes
        if self.route.startswith('/'):
            @self.app.route(self.route)
            def nodecdnjsurl():
                return "Works!"
        else: 
            print('[Flask] You must provide a leading slash before your route. ( ERROR on change_path() ) (default will be used)')
            self.route = '/nodecdn.js'
            @self.app.route(self.route)
            def nodecdnjsurl():
                return "Works!"