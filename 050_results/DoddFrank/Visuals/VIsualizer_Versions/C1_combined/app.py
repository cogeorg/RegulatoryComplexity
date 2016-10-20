#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
import os
import sys
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from apps import welcome
from apps import words
from apps import sentences


# add your project directory to the sys.path
project_home = os.getcwd()
if project_home not in sys.path:
    sys.path.append = project_home


# initiate the combined application
application = Flask(__name__)
application.config.update(
    TEMPLATES_AUTO_RELOAD = True
)

application.wsgi_app = DispatcherMiddleware(welcome, {
    '/words':           words,
    '/sentenceparts':   sentences
})

def extra_files():
    """
    Watch files and reload the server when they change.
    """

    extra_dirs = [
        'apps/sentences/templates/output'
    ]

    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)

    return extra_files

# run the application
if __name__ == "__main__":
    application.run(debug = True)

