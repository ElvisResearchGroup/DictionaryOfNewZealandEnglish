# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import *
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from DictionaryOfNewZealandEnglish.headword.models import *
from DictionaryOfNewZealandEnglish.headword.attribute.models import *
from DictionaryOfNewZealandEnglish.database import db
from sqlalchemy import asc, collate


class CitationForm(Form):
    date     = TextField('Date',         validators=[ DataRequired()])
    circa    = BooleanField('Circa')
    author   = TextField('Author',       validators=[ DataRequired(),
                                                     Length(max=50) ])

    # note: the source selection has had  ".filter_by(archived=False)" removed
    #   as on editing the citation, the source will become the first option
    #   on the drop down list. Not an acceptable solution.
    # Would need a more sophisticated sql query to remove 
    #   the archived sources and still leave the already selected option.
    source = QuerySelectField(
                   query_factory = lambda: db.session.query(Source)
                     .order_by(asc(collate(Source.name, 'NOCASE'))).all(),
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

