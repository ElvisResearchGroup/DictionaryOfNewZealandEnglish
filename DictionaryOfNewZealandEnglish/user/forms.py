from flask_wtf import Form
from wtforms import TextField, PasswordField, DateField, HiddenField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField

import sys
from .models import User

class RegisterForm(Form):
    username    = TextField('Username',
                                validators=[DataRequired(), 
                                            Length(min=3, max=25)])
    email       = TextField('Email',
                                validators=[DataRequired(), 
                                            Email(), 
                                            Length(min=6, max=40)])
    institution = TextField('Institution',
                                validators=[DataRequired(), 
                                            Length(min=6, max=40)])
    country     = TextField('Country',
                                validators=[DataRequired(),
                                            Length(min=2, max=40)])
    interest    = TextField('Interest',
                                validators=[DataRequired(),
                                            Length(min=6, max=300)])
    password    = PasswordField('Password',
                                validators=[DataRequired(), 
                                            Length(min=6, max=40)])
    confirm     = PasswordField('Verify password',
                                validators=[DataRequired(), 
                                            EqualTo('password', 
                                            message='Passwords must match')])
    updated_at  = HiddenField('updated_at')
    remember_me = BooleanField('Remember me')


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None


    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True
















