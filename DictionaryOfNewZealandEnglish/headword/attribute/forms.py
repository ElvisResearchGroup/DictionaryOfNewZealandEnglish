# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import DataRequired
from DictionaryOfNewZealandEnglish.headword.models import *


class TableEditForm(Form):
    name          = TextField('Name', validators=[DataRequired()])
    notes         = TextField('Notes',   validators=[DataRequired()])
    archived      = BooleanField('Archived')

    def __init__(self, *args, **kwargs):
        super(TableEditForm, self).__init__(*args, **kwargs)
        self.user = None

















