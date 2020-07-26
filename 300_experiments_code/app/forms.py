from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    student_id = StringField("Student ID", validators=[DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message = 'not the same password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already linked to another account.')

class RulesForm(FlaskForm):
    rules = BooleanField("I have read and understood the rules", validators= [DataRequired()])
    excel = BooleanField("I have tested the template and can open it", validators=[DataRequired()])
    submit = SubmitField("Continue")

class SubmissionForm(FlaskForm):
    answer = FloatField("Enter answer", validators = [DataRequired()])
    submit = SubmitField("Save and continue")
