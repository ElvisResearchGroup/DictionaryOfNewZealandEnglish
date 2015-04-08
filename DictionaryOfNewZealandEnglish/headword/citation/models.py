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

##############################################
# join tables for many-to-many relationships #
citation_source = db.Table('citation_source',
    db.Column('citation_id', db.Integer, db.ForeignKey('citations.id')),
    db.Column('source_id',   db.Integer, db.ForeignKey('sources.id'))
)


class Citation(SurrogatePK, Model):
    
    __tablename__ = "citations"
    date =       Column(db.String(20),   nullable=False)
    # per expert, circa needed as not all dates are accurate
    circa =      Column(db.Boolean,      default=False)
    author =     Column(db.String(80),   nullable=False)

    source_id =  ReferenceCol('sources', nullable=True)
    source =     relationship('Source',  backref='citations')

    vol_page =   Column(db.String(10),   nullable=True)
    edition =    Column(db.String(10),   nullable=True)
    quote =      Column(db.Text,         nullable=True)
    notes =      Column(db.Text,         nullable=True)
    archived =   Column(db.Boolean,      default=False)
    
    created_at = Column(db.DateTime,     default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime,     nullable=False)
    updated_by = Column(db.String(80),   nullable=False)


    def __init__(self, date, 
                       circa, 
                       author, 
                       source_id, 
                       vol_page, 
                       edition,
                       quote, 
                       notes, 
                       archived, 
 										   updated_at,
                       updated_by
                       ):

        db.Model.__init__(self, date              = date, 
                                circa             = circa, 
                                author            = author, 
                                source_id         = source_id, 
                                vol_page          = vol_page, 
                                edition           = edition,
                                quote             = quote, 
                                notes             = notes, 
                                archived          = archived, 
                                updated_at        = updated_at,
                                updated_by        = updated_by 
                                )

    @property
    def full_name(self):
        return "Citation is {0}".format(self.author)

    def __repr__(self):
        return '<Citation ({0}, {1})>'.format(self.author, self.date)

