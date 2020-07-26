To see what the website looks for now:

go to the directory (macbook cd ./Documents/wherever))
activate virtual environment : macbook ‘source venv/bin/activate’ or windows : ‘venv\Scripts\activate’

Install the necessary requirements. Once the venv is started, type: pip3 install -r requirements.txt
(To update requirements.txt from session where venv updated:pip freeze > requirements.txt)

tell flask how to import the app :
	-mac :  (venv) $ export FLASK_APP=regexp.py
	- windows : (venv) $ set FLASK_APP=regexp.py
- $ flask run
- open http://localhost:5000/ or http://localhost:5000/index


To access database from terminal: In python shell (typing "python" will open one):
- from app import db ; from app.models import User, Submission ;

then, for example, to see all the users in the database:
- users = User.query.all()
- for u in users: {print(u.username, u.email)}


In main folder:
- app
	- init.py
	- routes.py
	- models.py #defining database structure (users, submissions)
	- forms.py #defines the forms (register, login)
	- login.py #notused
	- templates
		- accept_rules.html #page after login/register
		- base.html
		- endpage.html
		- experiment.html
		- index.html
		- login.html
		- login2.html #(not used)
		- register.html
		- register2.html #(not used)
		- rules.html # page presenting the rules accessed from experiment page
- venv # virtual environment (Flask, jinja2, flask-bootstrap, doting)
- envvariablename.flaskenv : #is supposed to set FLASK_APP to regexp.py automatically (file read when ‘flask run’ in terminal), but doesn’t seem to work for now.
- regexp.py #automatic decoration of flask shell (python terminal shell more or less) doesn't work
