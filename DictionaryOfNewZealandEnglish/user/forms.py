from flask_wtf import Form
from wtforms import TextField, PasswordField, DateField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User

class RegisterForm(Form):
    username = TextField('Username',
             validators=[DataRequired(), Length(min=3, max=25)])
    email    = TextField('Email',
             validators=[DataRequired(), Email(), Length(min=6, max=40)])
    institution = TextField('Institution',
             validators=[DataRequired(), Length(min=6, max=40)])
    country  = TextField('Country',
             validators=[DataRequired(), Length(min=2, max=40)])
    interest = TextField('Interest',
             validators=[DataRequired(), Length(min=6, max=300)])
    password = PasswordField('Password',
             validators=[DataRequired(), Length(min=6, max=40)])
    confirm  = PasswordField('Verify password',
                [DataRequired(), EqualTo('password', message='Passwords must match')])
    updated_at = HiddenField('updated_at')
    remember_me = BooleanField('Remember me')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


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

    headword      = TextField('Headword', validators=[DataRequired()])
    definition    = TextField('Definition', validators=[DataRequired()])
    see           = TextField('See',   validators=[DataRequired()])
    pronunciation = TextField('Pronunciation',   validators=[DataRequired()])
    notes         = TextField('Notes',   validators=[DataRequired()])
    archived      = BooleanField('Archived')
    data_set_id   = TextField('Data_set_id',   validators=[DataRequired()])

    updated_at = HiddenField('updated_at')

    def __init__(self, *args, **kwargs):
        super(HeadwordForm, self).__init__(*args, **kwargs)
        self.user = None
        #self.used_as = "stuff"

    def validate(self):
      #if self.used_as.data == "insert_data":
        # TODO validations
        return True

        initial_validation = super(DataForm, self).validate()
        if not initial_validation:
            return "False 1"

        #self.author = User.query.filter_by(author=self.author.data).first()
        if not self.author.data:
            self.author.errors.append('Unknown author')
            return "False 2"

        if not self.source.data:
            self.source.errors.append('Must quote source')
            return "False 3"

        if not self.date.data:
            self.date.errors.append('Provide a date')
            return "False 4"

      #return "True"
