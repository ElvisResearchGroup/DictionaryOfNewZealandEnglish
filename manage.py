#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from waitress import serve

from DictionaryOfNewZealandEnglish.app import create_app
from DictionaryOfNewZealandEnglish.user.models import User
from DictionaryOfNewZealandEnglish.settings import DevConfig, ProdConfig
from DictionaryOfNewZealandEnglish.database import db

from DictionaryOfNewZealandEnglish.nzdc_data_import import nzdc_data_import
from DictionaryOfNewZealandEnglish.nzdc_data_massage import addNotesToDb, addStuffToDb, nzdc_resetdb, nzdc_seed
from DictionaryOfNewZealandEnglish.fixspaces import insert_most_missingSpaces


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
def data_import(myfile):
    nzdc_data_import(myfile)

@manager.command
def fix_spaces():
    insert_most_missingSpaces()


'''
This method (& file) may be removed once all data pre-processing is completed'''
#@manager.command
#def addNotesToDb(myfile):
#    addNotesToDb(myfile)

'''
This method (& file) may be removed once all data pre-processing is completed'''
#@manager.command
#def addStuff(myfile):
#    addStuffToDb(myfile)

'''
This method will ruin your day. (Only used in set-up). May be removed after pre-processing is completed'''
#@manager.command
#def resetdb():
#    nzdc_resetdb()

#@manager.command
#def seed():
#    nzdc_seed()

@manager.command
def runwaitress():
    '''
    Use waitress to serve the app.
    '''
    serve(app,host="0.0.0.0", port=8080)

@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
