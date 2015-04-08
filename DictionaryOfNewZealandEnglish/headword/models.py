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
headword_citations = db.Table('headword_citations',
    db.Column('headword_id', db.Integer, db.ForeignKey('headwords.id')),
    db.Column('citation_id', db.Integer, db.ForeignKey('citations.id'))
)
headword_flags = db.Table('headword_flags',
    db.Column('headword_id', db.Integer, db.ForeignKey('headwords.id')),
    db.Column('flag_id',     db.Integer, db.ForeignKey('flags.id'))
)
headword_registers = db.Table('headword_registers',
    db.Column('headword_id', db.Integer, db.ForeignKey('headwords.id')),
    db.Column('register_id',     db.Integer, db.ForeignKey('registers.id'))
)



class Headword(SurrogatePK, Model):

    __tablename__ = "headwords"
    headword =      Column(db.String(50), nullable=False)
    definition =    Column(db.Text,       nullable=False)
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



    domain_id =       ReferenceCol('domains', nullable=True)
    domain = relationship('Domain', backref='headwords')

    region_id =       ReferenceCol('regions', nullable=True)
    region = relationship('Region', backref='headwords')

    # M2M relations
    citations = relationship('Citation',
                             secondary = headword_citations,
                             backref=db.backref('headwords'),
                             order_by='Citation.archived, Citation.date')
    flags     = relationship('Flag', 
                             secondary = headword_flags,
                             backref=db.backref('headwords'),
                             order_by='Flag.name')
    registers = relationship('Register', 
                             secondary = headword_registers,
                             backref=db.backref('headwords'),
                             order_by='Register.name')

    created_at = Column(db.DateTime, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False)
    updated_by = Column(db.String(80), nullable=False)


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


