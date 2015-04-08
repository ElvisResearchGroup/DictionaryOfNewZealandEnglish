from flask_wtf import Form
from wtforms import *
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from DictionaryOfNewZealandEnglish.headword.models import *
from DictionaryOfNewZealandEnglish.headword.attribute.models import *
import sys
from DictionaryOfNewZealandEnglish.database import db


class HeadwordForm(Form):
                       #headword, 
                       #definition, 
                       #see, 
                       #pronunciation, 
                       #notes, 
                       #archived, 
                       #data_set_id, 
                       #homonym_number_id, 
                       #word_class_id, 
                       #sense_number_id, 
                       #origin_id, 
                       #register_id, 
                       #domain_id, 
                       #region_id, 
                       #headword_citation, 
                       #headword_flag, 
                       #updated_by

    headword      = TextField('Headword',       validators=[DataRequired(), 
                                                Length(max=50)])
    definition    = TextAreaField('Definition', validators=[DataRequired()])
    see           = TextField('See',            validators=[])
    pronunciation = TextField('Pronunciation',  validators=[])
    notes         = TextAreaField('Notes',      validators=[])
    archived      = BooleanField('Archived')
    
    # TODO place [none] option first
    word_class = QuerySelectField(
                   query_factory=lambda: db.session.query(Word_class).all(),
                   get_pk=lambda a: a.id,
                   get_label=lambda a: a.name )
    data_set = QuerySelectField(
                   query_factory=lambda: db.session.query(Data_set).all(),
                   get_pk=lambda a: a.id,
                   get_label=lambda a: a.name )
    homonym_number = QuerySelectField(
                   query_factory=lambda: db.session.query(Homonym_number).all(),
                   get_pk=lambda a: a.id,
                   get_label=lambda a: a.name )
    sense_number = QuerySelectField(
                   query_factory=lambda: db.session.query(Sense_number).all(),
                   get_pk=lambda a: a.id,
                   get_label=lambda a: a.name )
    origin = QuerySelectField(
                   query_factory=lambda: db.session.query(Origin).all(),
                   get_pk=lambda a: a.id,
                   get_label=lambda a: a.name )
    register = QuerySelectField(
                   query_factory=lambda: db.session.query(Register).all(),
                   get_pk=lambda a: a.id,
                   get_label=lambda a: a.name )
    domain = QuerySelectField(
                   query_factory=lambda: db.session.query(Domain).all(),
                   get_pk=lambda a: a.id,
                   get_label=lambda a: a.name )
    region = QuerySelectField(
                   query_factory=lambda: db.session.query(Region).all(),
                   get_pk=lambda a: a.id,
                   get_label=lambda a: a.name )
    flag = QuerySelectField(
                   query_factory=lambda: db.session.query(Flag).all(),
                   get_pk=lambda a: a.id,
                   get_label=lambda a: a.name )


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
'''
        #self.author = User.query.filter_by(author=self.author.data).first()
        if not self.author.data:
            self.author.errors.append('Unknown author')
            return False

        if not self.source.data:
            self.source.errors.append('Must quote source')
            return False

        if not self.date.data:
            self.date.errors.append('Provide a date')
            return False

      #return "True"
'''













