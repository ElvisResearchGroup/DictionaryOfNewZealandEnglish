from flask_wtf import Form
from wtforms import TextField, PasswordField, DateField, HiddenField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from DictionaryOfNewZealandEnglish.headword.models import *
import sys
from DictionaryOfNewZealandEnglish.database import db



class TableEditForm(Form):
    name          = TextField('Name', validators=[DataRequired()])
    notes         = TextField('Notes',   validators=[DataRequired()])
    archived      = BooleanField('Archived')

    def __init__(self, *args, **kwargs):
        super(TableEditForm, self).__init__(*args, **kwargs)
        self.user = None

















