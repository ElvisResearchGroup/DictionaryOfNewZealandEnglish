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

# TODO only keeping for reference, delete before release
#class Role(SurrogatePK, Model):
#    # roles = {'user', 'admin'}
#    __tablename__ = 'roles'
#    name = Column(db.String(80), unique=True, nullable=False)
#    user_id = ReferenceCol('users', nullable=True)
#    user = relationship('User', backref='roles')
#
#    def __init__(self, name, **kwargs):
#        db.Model.__init__(self, name=name, **kwargs)
#
#    def __repr__(self):
#        return '<Role({name})>'.format(name=self.name)

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
        # TODO active was inherited, is this used?
    is_admin =    Column(db.Boolean(), default=False)

    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, **kwargs)
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

# Copied from example above - delete when done
#    __tablename__ = 'roles'
#    name = Column(db.String(80), unique=True, nullable=False)
#    user_id = ReferenceCol('users', nullable=True)
#    user = relationship('User', backref='roles')
class Headword(SurrogatePK, Model):

    __tablename__ = "headwords"
    name =          Column(db.String(50), nullable=False)
    definition =    Column(db.Text, nullable=False)
    see =           Column(db.Text, nullable=True)
    pronunciation = Column(db.Text, nullable=True)
    notes =         Column(db.Text, nullable=True)
    archived =      Column(db.Boolean, default=False)
    
    data_set_id =       ReferenceCol('data_sets', nullable=True)
    data_set = relationship('Data_set', backref='headwords')
    
    homonym_number_id = ReferenceCol('homonym_numbers', nullable=True)
    homonym_number = relationship('Homonym_number', backref='headwords')

    word_class_id =       ReferenceCol('word_classes', nullable=True)
    word_class = relationship('Word_class', backref='headwords')

    sense_number_id =       ReferenceCol('sense_numbers', nullable=True)
    sense_number = relationship('Sense_number', backref='headwords')

    origin_id =       ReferenceCol('origins', nullable=True)
    origin = relationship('Origin', backref='headwords')

    register_id =       ReferenceCol('registers', nullable=True)
    register = relationship('Register', backref='headwords')
# TODO not trusting this works first time
#    register2_id =       ReferenceCol('registers', nullable=True)
#    register = relationship('Register', backref='headwords')

    domain_id =       ReferenceCol('domains', nullable=True)
    domain = relationship('Domain', backref='headwords')

    region_id =       ReferenceCol('regions', nullable=True)
    region = relationship('Region', backref='headwords')
# TODO many to many - likely needs more work
#    headword_flag_id =       ReferenceCol('headword_flags', nullable=True)
#    headword_flag = relationship('Headword_flag', backref='headwords')

#    headword_citation_id =       ReferenceCol('headword_citations', nullable=True)
#    headword_citation = relationship('Headword_citation', backref='headwords')

    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at =     Column(db.DateTime, nullable=False)
    last_update_by = Column(db.String(80), nullable=False)
    
    @property
    def full_name(self):
        return "Headword is {0}".format(self.name)

    def __repr__(self):
        return '<Headword ({name!r})>'.format(name=self.name)

class Citation(SurrogatePK, Model):
    
    __tablename__ = "citations"
    #_id = Column(db.Integer, primary_key=True)
    author = Column(db.String(80), nullable=False)
    source = Column(db.String(80), nullable=False)
    date = Column(db.DateTime)

    def __init__(self, author, source, date, **kwargs):
        db.Model.__init__(self, author=author, source=source, date=date, **kwargs)

    @property
    def cite(self):
        return "{0} {1} {2}".format(self.author, self.source, self.date)

    def __repr__(self):
        #return 'hello'
        return "<Citation({citeme})>".format(citeme=self.cite)
        #return "{0} {1} {2}".format(self.author, self.source, self.date)
        #return self.cite

