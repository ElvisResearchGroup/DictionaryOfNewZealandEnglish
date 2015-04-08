#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import datetime as dt
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

from DictionaryOfNewZealandEnglish.app import create_app
from DictionaryOfNewZealandEnglish.user.models import *
from DictionaryOfNewZealandEnglish.headword.models import *
from DictionaryOfNewZealandEnglish.headword.attribute.models import *
from DictionaryOfNewZealandEnglish.headword.citation.models import *
from DictionaryOfNewZealandEnglish.settings import DevConfig, ProdConfig
from DictionaryOfNewZealandEnglish.database import db

if os.environ.get("DICTIONARYOFNEWZEALANDENGLISH_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}

@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

# TODO add a condition to return nil if in production
@manager.command
def resetdb():
    # if in production return nil
    print "#### removing old files"
    subprocess.call(["rm", "dev.db"])
    subprocess.call(["rm", "-r", "migrations"])
    print "#### init db"
    subprocess.call(["python", "manage.py", "db", "init"])
    print "#### migrate db"
    subprocess.call(["python", "manage.py", "db", "migrate"])
    print "#### upgrade db"
    subprocess.call(["python", "manage.py", "db", "upgrade"])
    print "#### seed db"
    subprocess.call(["python", "manage.py", "seed"])
    print "#### done"


# Seed data for initialising the secondary tables of the database
# Also Users 'admin' and 'Matt'
# Also Headword entry 'test'
# might not be the Python place for it, but it works :-)
@manager.command
def seed():
    seed_date = dt.datetime.utcnow()
    User.create( username="admin", 
                 email="admin@example.com", 
                 institution="NZDC VUW",
                 country="NZ",
                 interest="Admin role",
                 is_admin=True,
                 password="qwerty", 
                 updated_at=seed_date,
                 active=True )
    User.create( username="matt", 
                 email="matt@example.com", 
                 institution="NZDC VUW",
                 country="NZ",
                 interest="user role",
                 password="qwerty", 
                 updated_at=seed_date,
                 active=True )

    Headword.create(
                 headword="test",
                 definition="try me",
                 see="Big ball of mud",
                 pronunciation="as written",
                 notes="testing is good for the soul.",
                 data_set_id=3,
                 homonym_number_id=20, 
                 word_class_id=27,
                 sense_number_id=59, 
                 origin_id=16, 
                 #register_id=16, 
                 domain_id=26, 
                 region_id=7, 
                 updated_at=seed_date,
                 updated_by="seed"
                   )

    Headword.create(
                 headword="cat",
                 definition="furry and noisy",
                 see="",
                 pronunciation="caaaat",
                 notes="do not startle",
                 data_set_id=3,
                 homonym_number_id=20, 
                 word_class_id=27,
                 sense_number_id=59, 
                 origin_id=16, 
                 #register_id=16, 
                 domain_id=26, 
                 region_id=7, 
                 updated_at=seed_date,
                 updated_by="seed"
                   )

    Citation.create(
                 date       = "1/1/1972",
                 circa      = 0,
                 author     = "Matt",
                 source_id  = 2,
                 vol_page   = "1/253",
                 edition    = "5",
                 quote      = "The amber elixer of life",
                 notes      = "Beer",
                 archived   = False,
                 updated_at = seed_date,
                 updated_by = "seed"
                   )

    Citation.create(
                 date       = "1/2/1972",
                 circa      = 0,
                 author     = "Matt",
                 source_id  = 2,
                 vol_page   = "",
                 edition    = "",
                 quote      = "Love the smell of napalm in the morning.",
                 notes      = "",
                 archived   = False,
                 updated_at = seed_date,
                 updated_by = "seed"
                   )
    
    h = Headword.query.get(1)
    h.citations.append(Citation.query.get(1))
    h.citations.append(Citation.query.get(2))

    Flag.create( id=0,
                 name="[none]",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Flag.create( id=1,
                 name="Transport",
                 notes="DB",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Flag.create( id=2,
                 name="Slang",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Flag.create( id=3,
                 name="Farm Words",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Flag.create( id=4,
                 name="Geology",
                 notes="Geology",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")

    h = Headword.query.get(1)
    h.flags.append(Flag.query.get(1))
    h.flags.append(Flag.query.get(4))
    h = Headword.query.get(2)
    h.flags.append(Flag.query.get(1))

    Homonym_number.create( id=11,
                 name="1",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Homonym_number.create( id=18,
                 name="2",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Homonym_number.create( id=19,
                 name="3",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Homonym_number.create( id=20,
                 name="4",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Homonym_number.create( id=22,
                 name="5",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Homonym_number.create( id=23,
                 name="6",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Homonym_number.create( id=24,
                 name="7",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Homonym_number.create( id=25,
                 name="8",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Homonym_number.create( id=26,
                 name="9",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")

    Word_class.create( id=0,
                 name="[none]",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=69,
                 name="[_none_]",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=39,
                 name="abbreviation",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=12,
                 name="adjective",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=17,
                 name="adverb",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=27,
                 name="conjunction",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=71,
                 name="determiner",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=23,
                 name="exclamation",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=1,
                 name="noun",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=9,
                 name="phrase",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=73,
                 name="prefix",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=30,
                 name="preposition",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=8,
                 name="pronoun",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Word_class.create( id=13,
                 name="verb",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")

    Sense_number.create( id=2,
                 name="1",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Sense_number.create( id=25,
                 name="2",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Sense_number.create( id=37,
                 name="3",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Sense_number.create( id=48,
                 name="4",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Sense_number.create( id=59,
                 name="5",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Sense_number.create( id=70,
                 name="6",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Sense_number.create( id=80,
                 name="7",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Sense_number.create( id=91,
                 name="8",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Sense_number.create( id=101,
                 name="9",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")

    Register.create( id=1,
                 name="[none]",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=19,
                 name="archaic",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=16,
                 name="corse slang",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=9,
                 name="dated",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=11,
                 name="derogatory",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=15,
                 name="ephemistic",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=4,
                 name="formal",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=6,
                 name="historical",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=14,
                 name="humorous",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=5,
                 name="informal",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=12,
                 name="literary",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=20,
                 name="obsolete",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=7,
                 name="offensive",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=13,
                 name="rare",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Register.create( id=17,
                 name="trademark",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")

    h = Headword.query.get(1)
    h.registers.append(Register.query.get(12))
    h.registers.append(Register.query.get(16))
    h = Headword.query.get(2)
    h.registers.append(Register.query.get(13))

    Domain.create( id=1,
                 name="[none]",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Domain.create( id=16,
                 name="Commerce",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Domain.create( id=4,
                 name="Cuisine",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Domain.create( id=8,
                 name="Environment",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Domain.create( id=5,
                 name="Geology",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Domain.create( id=12,
                 name="Marine",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Domain.create( id=20,
                 name="Media",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Domain.create( id=27,
                 name="Politics",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Domain.create( id=3,
                 name="Rural",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Domain.create( id=26,
                 name="Science",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Domain.create( id=6,
                 name="Sport",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")

    Region.create( id=1,
                 name="[none]",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Region.create( id=3,
                 name="New Zealand and Australia",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Region.create( id=7,
                 name="New Zealand (Southern South Island)",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Region.create( id=8,
                 name="New Zealand (Weat Coast South Island)",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Region.create( id=9,
                 name="New Zealand and Pacific",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")


    Origin.create( id=2,
                 name="[none]",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=18,
                 name="abbreviation",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=10,
                 name="Aboriginal",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=8,
                 name="acronym",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=19,
                 name="blend",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=11,
                 name="British dialect",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=12,
                 name="catchphrase",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=17,
                 name="ellipsis",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=22,
                 name="eponym",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=15,
                 name="euphemism",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=16,
                 name="expletive",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=14,
                 name="initialism",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=4,
                 name="Maori",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=21,
                 name="Moriori",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=7,
                 name="Polynesian",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=9,
                 name="rhyming slang",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=5,
                 name="Samoan",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=6,
                 name="Tongan",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Origin.create( id=23,
                 name="toponym",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")

    Data_set.create( id=0,
                 name="[none]",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Data_set.create( id=1,
                 name="Orsman",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Data_set.create( id=2,
                 name="DNZE",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Data_set.create( id=3,
                 name="Incomings",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")

    Source.create( id=0,
                 name="[none]",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Source.create( id=1,
                 name="NZ TV Times",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Source.create( id=2,
                 name="Wellington Craft Beers Monthly",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")
    Source.create( id=3,
                 name="On the Search for Dragons",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="seed")


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
