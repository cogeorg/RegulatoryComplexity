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

Major Updates (18/01/2021):

1. CorrectAnswer database model was created in models.py
	 - This is used to reference submited answers vs correct answers in DB in order to get a final score for the users.
	 - It is also used on the end page to show a breakdown of the users answers.
2. PracticeForm wtf form created in forms.py
	 - Used to seperate actual test from practice test.
	 - The forms display logic can be found in routes.py. 
	 - Javascript is used to check submitted answer against correct practice answer as set in the experiments.html page. See below.
3. Refer to commented tags in experiments.html for step by step information relating to how the experiments page functions. 
