from flask_wtf import Form
from wtforms import *
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from DictionaryOfNewZealandEnglish.headword.models import *
from DictionaryOfNewZealandEnglish.headword.attribute.models import *
import sys
from DictionaryOfNewZealandEnglish.database import db


class CitationForm(Form):
    date     = TextField('Date',         validators=[ DataRequired()])
    circa    = BooleanField('Circa')
    author   = TextField('Author',       validators=[ DataRequired(),
                                                     Length(max=50) ])
    source = QuerySelectField(
                   query_factory = lambda: db.session.query(Source).all(),
                   get_pk        = lambda a: a.id,
                   get_label     = lambda a: a.name )
    vol_page = TextField('Volume/Page',  validators=[ Length(max=10) ])
    edition  = TextField('Edition',      validators=[ Length(max=10) ])
    quote    = TextAreaField('Quote',    validators=[ ])
    notes    = TextAreaField('Notes',    validators=[ ])
    archived = BooleanField('Archived')


    def getattr(self, name):
        return getattr(self, name)    


    def __init__(self, *args, **kwargs):
        super(CitationForm, self).__init__(*args, **kwargs)
        self.user = None


    def validate(self):
        initial_validation = super(CitationForm, self).validate()
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













