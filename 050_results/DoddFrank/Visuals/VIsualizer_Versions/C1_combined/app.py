#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
import os
import sys
from werkzeug.wsgi import DispatcherMiddleware
from apps import welcome
from apps import words
from apps import sentences


# add your project directory to the sys.path
project_home = os.getcwd()
if project_home not in sys.path:
    sys.path.append = project_home


# initiate the combined application
application = Flask(__name__)

application.wsgi_app = DispatcherMiddleware(welcome, {
    '/words':           words,
    '/sentenceparts':   sentences
})

# run the application
if __name__ == "__main__":
    application.run(debug = True)

