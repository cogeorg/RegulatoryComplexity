#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:00:21 2019

@author: jane
"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bootstrap = Bootstrap(app)

login = LoginManager(app)
login.login_view = 'login'


from app import routes, models
