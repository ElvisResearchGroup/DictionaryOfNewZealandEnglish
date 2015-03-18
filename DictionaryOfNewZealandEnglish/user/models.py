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

    def __init__(self, username, email, institution, country, interest, updated_at, password=None, active=False, is_admin=False):

        db.Model.__init__(self, 
                          username=username, 
                          email=email, 
                          institution=institution,
                          country=country,
                          interest=interest,
													updated_at=updated_at,
                          active=active,
                          is_admin=is_admin)
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


##############################################
# join tables for many-to-many relationships #
headword_flags = db.Table('headword_flags',
    db.Column('headword_id', db.Integer, db.ForeignKey('headwords.id')),
    db.Column('flag_id',     db.Integer, db.ForeignKey('flags.id'))
)

headword_citations = db.Table('headword_citations',
    db.Column('headword_id', db.Integer, db.ForeignKey('headwords.id')),
    db.Column('citation_id', db.Integer, db.ForeignKey('citations.id'))
)

# citation_sources



class Headword(SurrogatePK, Model):
    #################################
    ## start - table column set-up ##
    __tablename__ = "headwords"
    headword =      Column(db.String(50), nullable=False)
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

# TODO many to many - may need more work
#    headword_citation = relationship('Citation', secondary = headword_citations,
#        backref=db.backref('citations', lazy='dynamic'))
#    headword_flag = relationship('Flag', secondary = headword_flags,
#        backref=db.backref('headwords', lazy='dynamic'))

    created_at = Column(db.DateTime, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False)
    updated_by = Column(db.String(80), nullable=False)
    ## end - table column setup ##
    ##############################


    def __init__(self, headword, 
                       definition, 
                       see, 
                       pronunciation, 
                       notes, 
                       data_set_id,
                       homonym_number_id, 
                       word_class_id, 
                       sense_number_id, 
                       origin_id, 
                       register_id, 
                       domain_id, 
                       region_id, 
 										   updated_at,
                       updated_by
                       ):

        db.Model.__init__(self, headword         =headword, 
                                definition       =definition, 
                                see              =see, 
                                pronunciation    =pronunciation, 
                                notes            =notes, 
                                data_set_id      =data_set_id,
                                homonym_number_id=homonym_number_id, 
                                word_class_id    =word_class_id, 
                                sense_number_id  =sense_number_id, 
                                origin_id        =origin_id, 
                                register_id      =register_id,          
                                domain_id        =domain_id, 
                                region_id        =region_id, 
                                updated_at       =updated_at,
                                updated_by       =updated_by 
                                )

    @property
    def full_name(self):
        return "Headword is {0}".format(self.headword)

    def __repr__(self):
        return '<Headword ({name!r})>'.format(name=self.headword)



class Citation(SurrogatePK, Model):
    
    __tablename__ = "citations"
    date =       Column(db.DateTime,   nullable=False)
    # per expert, circa needed as not all dates are accurate
    circa =      Column(db.Boolean, default=False)
    author =     Column(db.String(80), nullable=False)

    source_id =  ReferenceCol('sources', nullable=True)
    source =     relationship('Source', backref='citations')

    vol_page =   Column(db.String(50), nullable=True)
    edition =    Column(db.String(50), nullable=True)
    quote =      Column(db.Text,       nullable=True)
    notes =      Column(db.Text,       nullable=True)
    archived =      Column(db.Boolean, default=False)
    
    created_at = Column(db.DateTime,   default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime,   nullable=False)
    updated_by = Column(db.String(80), nullable=False)


    def __init__(self, author, source, date, **kwargs):
        db.Model.__init__(self, author=author, source=source, date=date, **kwargs)

    @property
    def full_name(self):
        return "{0} {1} {2}".format(self.author, self.source, self.date)

    def __repr__(self):
        return "<Citation({name!r})>".format(name=self.full_name)

###################################
# superclass for secondary tables #
class Secondary_values():
    
    name       = Column(db.String(50), nullable=False, unique=True)
    notes      = Column(db.Text,       nullable=True)
    archived   = Column(db.Boolean,    default=False)
    created_at = Column(db.DateTime,   default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime,   nullable=False)
    updated_by = Column(db.String(80), nullable=False)

    def __init__(self, name, notes, updated_by, updated_at, archived=False, id=None ):
        db.Model.__init__(self, 
                          name=name, 
                          notes=notes,  
                          updated_at=updated_at, 
                          updated_by=updated_by,
                          archived=archived,
                          id=id)

    @property
    def full_name(self):
        return "%s" % self.name

    def __repr__(self):
        return "<%s (%s, '%s')>" % (self.__name__, self.id, self.name)

####################
# secondary tables #
class Word_class(Secondary_values, SurrogatePK, Model):
    __name__ = 'Word_class'
    __tablename__ = "word_classes"

class Data_set(Secondary_values, SurrogatePK, Model):
    __name__ = 'Data_set'
    __tablename__ = "data_sets"

class Sense_number(Secondary_values, SurrogatePK, Model):
    __name__ = 'Sense_number'
    __tablename__ = "sense_numbers"

class Homonym_number(Secondary_values, SurrogatePK, Model):
    __name__ = 'Homonym_number'
    __tablename__ = "homonym_numbers"

class Register(Secondary_values, SurrogatePK, Model):
    __name__ = 'Register'
    __tablename__ = "registers"

class Domain(Secondary_values, SurrogatePK, Model):
    __name__ = 'Domain'
    __tablename__ = "domains"

class Region(Secondary_values, SurrogatePK, Model):
    __name__ = 'Region'
    __tablename__ = "regions"

class Origin(Secondary_values, SurrogatePK, Model):
    __name__ = 'Origin'
    __tablename__ = "origins"

class Flag(Secondary_values, SurrogatePK, Model):
    __name__ = 'Flag'
    __tablename__ = "flags"

class Source(Secondary_values, SurrogatePK, Model):
    __name__ = 'Source'
    __tablename__ = "sources"




