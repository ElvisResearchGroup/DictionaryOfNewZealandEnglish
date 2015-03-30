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

