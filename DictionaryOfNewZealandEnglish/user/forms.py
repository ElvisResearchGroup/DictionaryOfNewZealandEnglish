# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, PasswordField, HiddenField, BooleanField
from wtforms.validators import *

import sys
from .models import User

class RegisterForm(Form):
    username    = TextField('Username',
                                validators=[DataRequired(), 
                                            Length(min=3, max=25)])
    email       = TextField('Email',
                                validators=[DataRequired(), 
                                            Email()])
    institution = TextField('Institution',
                                validators=[DataRequired(), 
                                            Length(min=2, max=40)])
    country     = TextField('Country',
                                validators=[DataRequired(),
                                            Length(min=2, max=40)])
    interest    = TextField('Interest',
                                validators=[DataRequired(),
                                            Length(min=2, max=300)])
    password    = PasswordField('Password',
                                validators=[DataRequired(), 
                                            Length(min=6, max=40)])
    confirm     = PasswordField('Verify password',
                                validators=[DataRequired(), 
                                            EqualTo('password', 
                                            message='Passwords must match')])
    updated_at  = HiddenField('updated_at')


    def getattr(self, name):
        return getattr(self, name)    

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


class UserForm(Form):
    username    = TextField('Username',
                                validators=[Length(min=3, max=25)])
    email       = TextField('Email',
                                validators=[Optional(), Email()])
    institution = TextField('Institution',
                                validators=[Length(min=2, max=40)])
    country     = TextField('Country',
                                validators=[Length(min=2, max=40)])
    interest    = TextField('Interest',
                                validators=[Length(min=2, max=300)])
    password    = PasswordField('Password', 
                                validators=[#DataRequired(),
                                            Optional(), 
                                            Length(min=6, max=40)])
    confirm     = PasswordField('Verify password',
                                validators=[ 
                                            EqualTo('password', 
                                            message='Passwords must match')])
    updated_at  = HiddenField('updated_at')


    def getattr(self, name):
        return getattr(self, name)    

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user = None


    def validate(self):
        initial_validation = super(UserForm, self).validate()
        if not initial_validation:
            return False

#        user = User.query.filter_by(email=self.email.data).first()
#        if user and self.email.data:
#            self.email.errors.append("Email already registered")
#            return False

        if self.password.data != '':
            password = self.password.data
            if len(password) < 6 or 40 < len(password):
                self.password.errors.append("Password should be 6 to 40 characters")
                return False

        return True


class SearchForm(Form):
    email       = TextField('Email', validators=[Email(), 
                                     Length(min=6, max=40)])
    fish        = BooleanField('Is admin?')    


    def getattr(self, name):
        return getattr(self, name)    

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.user = None


class AdminForm(Form):
    email       = HiddenField('Email', validators=[Email(), 
                                     Length(min=6, max=40)])
    is_admin    = BooleanField('Is an administrator?')    
    delete_user = BooleanField('Delete user?')    


    def getattr(self, name):
        return getattr(self, name)    

    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.user = None

















