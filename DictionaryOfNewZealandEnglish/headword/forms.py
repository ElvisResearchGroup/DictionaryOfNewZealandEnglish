# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import *
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from DictionaryOfNewZealandEnglish.headword.models import *
from DictionaryOfNewZealandEnglish.headword.attribute.models import *
from DictionaryOfNewZealandEnglish.database import db
from sqlalchemy import asc, collate

class SearchForm(Form):
    headword         = TextField('Headword',    validators=[DataRequired(), 
                                                Length(max=50)])
    output = RadioField('Output', 
                        choices=[('definition_only', 'definition only'),
                                 ('sample_citations', 'sample citations'),
                                 ('all_citations', 'all citations')],
                        default = 'sample_citations')

    def getattr(self, name):
        return getattr(self, name)    

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.user = None


class HeadwordForm(Form):
    headword      = TextField('Headword',       validators=[DataRequired(), 
                                                Length(max=50)])
    definition    = TextAreaField('Definition', validators=[DataRequired()])
    see           = TextField('See',            validators=[])
    pronunciation = TextField('Pronunciation',  validators=[])
    notes         = TextAreaField('Notes',      validators=[])
    archived      = BooleanField('Archived')
    
    word_class = QuerySelectField(
                   query_factory=lambda: db.session.query(Word_class)
                     .order_by(asc(collate(Word_class.name, 'NOCASE'))).all(),
                   get_pk       =lambda a: a.id,
                   get_label    =lambda a: a.name, 
                   allow_blank=True,
                   blank_text="none" )
    data_set = QuerySelectField(
                   query_factory=lambda: db.session.query(Data_set)
                     .order_by(asc(collate(Data_set.name, 'NOCASE'))).all(),
                   get_pk       =lambda a: a.id,
                   get_label    =lambda a: a.name, 
                   allow_blank=True,
                   blank_text="none")
    homonym_number = QuerySelectField(
                   query_factory=lambda: db.session.query(Homonym_number)
                     .order_by(asc(collate(Homonym_number.name, 'NOCASE'))).all(),
                   get_pk       =lambda a: a.id,
                   get_label    =lambda a: a.name, 
                   allow_blank=True,
                   blank_text="none" )
    sense_number = QuerySelectField(
                   query_factory=lambda: db.session.query(Sense_number)
                     .order_by(asc(collate(Sense_number.name, 'NOCASE'))).all(),
                   get_pk       =lambda a: a.id,
                   get_label    =lambda a: a.name, 
                   allow_blank=True,
                   blank_text="none" )
    origin = QuerySelectField(
                   query_factory=lambda: db.session.query(Origin)
                     .order_by(asc(collate(Origin.name, 'NOCASE'))).all(),
                   get_pk       =lambda a: a.id,
                   get_label    =lambda a: a.name, 
                   allow_blank=True,
                   blank_text="none" )
    register = QuerySelectField(
                   query_factory=lambda: db.session.query(Register)
                      .order_by(asc(collate(Register.name, 'NOCASE'))).all(),
                   get_pk       =lambda a: a.id,
                   get_label    =lambda a: a.name, 
                   allow_blank=True,
                   blank_text="none" )
    domain = QuerySelectField(
                   query_factory=lambda: db.session.query(Domain)
                      .order_by(asc(collate(Domain.name, 'NOCASE'))).all(),
                   get_pk       =lambda a: a.id,
                   get_label    =lambda a: a.name, 
                   allow_blank=True,
                   blank_text="none" )
    region = QuerySelectField(
                   query_factory=lambda: db.session.query(Region).filter_by(archived=False)
                      .order_by(asc(collate(Region.name, 'NOCASE'))).all(),
                   get_pk       =lambda a: a.id,
                   get_label    =lambda a: a.name, 
                   allow_blank=True,
                   blank_text="none" )
    flag = QuerySelectField(
                   query_factory=lambda: db.session.query(Flag).filter_by(archived=False)
                      .order_by(asc(collate(Flag.name, 'NOCASE'))).all(),
                   get_pk       =lambda a: a.id,
                   get_label    =lambda a: a.name, 
                   allow_blank=True,
                   blank_text="none" )


    def getattr(self, name):
        return getattr(self, name)    


    def __init__(self, *args, **kwargs):
        super(HeadwordForm, self).__init__(*args, **kwargs)
        self.user = None


    def validate(self):

        initial_validation = super(HeadwordForm, self).validate()
        if not initial_validation:
            return False

        return True













