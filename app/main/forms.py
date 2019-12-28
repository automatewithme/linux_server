from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask import request
'''
The Flask-WTF extension uses Python classes to represent web forms.
A form class simply defines the fields of the form as class variables.
'''


class JobapplicationForm(FlaskForm):
    name = TextAreaField('Name', validators=[
        DataRequired(), Length(min=1, max= 35)])
    position = TextAreaField('Position', validators=[
        DataRequired(), Length(min=1, max= 35)])
    location = TextAreaField('Location', validators=[
        DataRequired(), Length(min=1, max= 35)])
    duration = TextAreaField('Duration', validators=[
        DataRequired(), Length(min=1, max= 35)])
    stipend = TextAreaField('Stipend', validators=[
        DataRequired(), Length(min=1, max= 35)])
    deadline = TextAreaField('Deadline', validators=[
        DataRequired(), Length(min=1, max= 35)])
    submit = SubmitField('Register')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username


    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)