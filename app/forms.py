from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, IntegerField, FieldList, FormField, TextAreaField
from wtforms.validators import  DataRequired, ValidationError, Email, EqualTo, NumberRange, Optional, Length
from app.models import Admin, WorkshopActivity
import datetime


'''
This module contains classes that extend FlaskForm and 
define the content of post requests that users may send to the app in order to: 
    log administrators in
    register new administrators
    create new workshops
    add post-its to a workshop's timeline.
'''

class AdminLoginForm(FlaskForm):
    '''
    The administrator log in form contains a username, password, and remember me field.
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AdminRegistration(FlaskForm):
    '''
    The administrator registration form contains a  
    '''
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=128)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Admin.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Admin.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class WorkshopCreationForm(FlaskForm): 
    name = StringField('Workshop Name', validators=[DataRequired(), Length(max=100)])
    date = DateField(
        'Workshop Date', 
        validators=[DataRequired()], 
        format='%m-%d-%y',  
        default=datetime.date(
            datetime.date.today().year, 
            datetime.date.today().month, 
            datetime.date.today().day))
    question = StringField('Question for participants', validators=[DataRequired(), Length(max=140)])
    unique_str = StringField(
        'Unique Session String',
        description="A short sequence of characters that your workshop participants will use to access the session.",
        validators=[DataRequired(), Length(max=20)])
    unit_is_year = SelectField('Timeline Style', choices=[("year", "Yearlong"), ("life", "Lifelong")])
    submit = SubmitField('Create Workshop Session')

    def validate_unique_str(self, unique_str): 
        ws = WorkshopActivity.query.filter_by(unique_str=unique_str.data).first()
        if ws is not None: 
            raise ValidationError('Please use a different unique string.')


class SingleTimelineEntryGeneral(FlaskForm):
    body = TextAreaField('Post-It Body', validators=[Optional(), Length(max=500)])
    on_sex = SelectField('Entry Type', choices=[("sex", 'Sexuality'), ("gender", 'Gender')])


class SingleTimelineEntryLifelong(SingleTimelineEntryGeneral):
    timestamp = IntegerField(
        'Age', validators=[Optional(), NumberRange(min=0, message="Age cannot be negative!")])


class SingleTimelineEntryYearlong(SingleTimelineEntryGeneral):
    timestamp = DateField('Time of Year (MM-DD)', format='%m-%d', validators=[Optional()])


class ContributeToTimelineYearlong(FlaskForm):
    submissions = FieldList(FormField(SingleTimelineEntryYearlong), min_entries=5, validators=[Optional()])
    submit = SubmitField('Submit')


class ContributeToTimelineLifelong(FlaskForm):
    submissions = FieldList(FormField(SingleTimelineEntryLifelong), min_entries=5, validators=[Optional()])
    submit = SubmitField('Submit')