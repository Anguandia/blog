from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField, Field
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User, Post

class LoginForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Name Used')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email Used')

class PostForm(FlaskForm):
    post = TextAreaField('Please write your post', validators=[Length(min=1, max=140)])
    questionID = StringField('', validators=[DataRequired()])
    submit = SubmitField('Post')

#class QuestionForm(FlaskForm):
 #   question = TextAreaField('Please write your post', validators=[Length(min=1, max=140)])
  #  submit = SubmitField('Post')