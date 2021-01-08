from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, IntegerField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from app.models import CorrectAnswer

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
    submit = SubmitField("Continue", render_kw={"onclick": "reset_timer()"})

class PracticeForm(FlaskForm):
    answer = FloatField("Enter the bank's total risk weighted assets for this regulation:", validators = [DataRequired()])
    n_reg  = HiddenField(id="n_reg", validators = [DataRequired()])
    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        correctanswer = CorrectAnswer.query.filter_by(correctanswer=self.answer.data, id=self.n_reg.data).first()
        if correctanswer is None:
            self.answer.errors.append('This answer is incorrect. Input 1.00 to continue. The next 9 questions will not evaluate your answer so think carefully before answering.')
            return False

        return True

    submit = SubmitField("Save and continue", render_kw={"onclick": "reset_timer()"})
    

class SubmissionForm(FlaskForm):
    answer = FloatField("Enter the bank's total risk weighted assets for this regulation:", validators = [DataRequired()])
    n_reg  = HiddenField(id="n_reg", validators = [DataRequired()])
    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        return True

    submit = SubmitField("Save and continue", render_kw={"onclick": "reset_timer()"})
    
