# -*- coding: utf-8 -*-
import datetime as dt

from flask.ext.login import UserMixin

from DictionaryOfNewZealandEnglish.extensions import bcrypt
from DictionaryOfNewZealandEnglish.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)


class User(UserMixin, SurrogatePK, Model):

    __tablename__ = 'users'
    username =    Column(db.String(80), unique=True, nullable=False)
    email =       Column(db.String(80), unique=True, nullable=False)
    first_name =  Column(db.String(30), nullable=True)
    last_name =   Column(db.String(30), nullable=True)
    institution = Column(db.String(50), nullable=True)
    country =     Column(db.String(50), nullable=True)
    interest =    Column(db.Text,       nullable=True)

    password =    Column(db.String(128), nullable=True) # The hashed password
    active =      Column(db.Boolean(), default=False) 
    
    is_admin =    Column(db.Boolean(), default=False)

    created_at = Column(db.DateTime, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False)


    def __init__(self, 
                 username, email, 
                 institution, 
                 country, 
                 interest,
                 updated_at,
                 password=None,
                 active=False,
                 is_admin=False):

        db.Model.__init__(self, 
                          username    = username, 
                          email       = email, 
                          institution = institution,
                          country     = country,
                          interest    = interest,
													updated_at  = updated_at,
                          active      = active,
                          is_admin    = is_admin)
        if password:
            self.set_password(password)
        else:
            self.password = None


    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)


    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)


    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)


    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)




