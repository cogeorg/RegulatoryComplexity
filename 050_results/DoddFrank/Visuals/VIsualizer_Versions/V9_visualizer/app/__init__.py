from flask import Flask
import os
from flask_mail import Mail
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = os.urandom(12)


mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'regulatorycomplexity@gmail.com'
app.config['MAIL_PASSWORD'] = 'baseliii'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


from app import views
# from app import titles
