from flask import Flask
import os
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = os.urandom(12)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'alij.limon@gmail.com'
app.config['MAIL_PASSWORD'] = 'bundesbank'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


from app import views
from app import titles
