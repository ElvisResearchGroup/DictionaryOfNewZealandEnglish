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


###################################
# superclass for attributes #
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
# attributes #
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

class Domain(Secondary_values, SurrogatePK, Model):
    __name__ = 'Domain'
    __tablename__ = "domains"

class Region(Secondary_values, SurrogatePK, Model):
    __name__ = 'Region'
    __tablename__ = "regions"

class Origin(Secondary_values, SurrogatePK, Model):
    __name__ = 'Origin'
    __tablename__ = "origins"

class Register(Secondary_values, SurrogatePK, Model):
    __name__ = 'Register'
    __tablename__ = "registers"

    def __repr__(self):
        return "%s" % self.name

class Flag(Secondary_values, SurrogatePK, Model):
    __name__ = 'Flag'
    __tablename__ = "flags"

    def __repr__(self):
        return "%s" % self.name

# used by citations #
class Source(Secondary_values, SurrogatePK, Model):
    __name__ = 'Source'
    __tablename__ = "sources"




