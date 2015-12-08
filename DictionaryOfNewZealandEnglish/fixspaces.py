# -*- coding: utf-8 -*-

'''
Helper function for fixing accidentally concatinated words in
Headword definition, Notes and Quotes.
'''

from DictionaryOfNewZealandEnglish.headword.citation.models import Citation
from DictionaryOfNewZealandEnglish.headword.models import Headword
from DictionaryOfNewZealandEnglish.settings import Config
from enchant.checker import SpellChecker
from DictionaryOfNewZealandEnglish.database import db
import multiprocessing as mp
from functools import partial
from collections import deque

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from DictionaryOfNewZealandEnglish.settings import ProdConfig

#Initialise dictionary
checker = SpellChecker(Config.SPELLCHECK_LANG)

# Set multiprocessing
MUTLIP = True

def fixline(text):
    '''
    Takes text with concatinated words and does it's best to put the
    spaces back in using the pyenchant SPELLCHECK_LANG dictionary.
    Derived from:
    http://stackoverflow.com/questions/23314834/tokenizing-unsplit-words-from-ocr-using-nltk
    '''
    checker.set_text(text)
    for error in checker:
        for suggestion in error.suggest():
            if error.word.replace(' ', '') == suggestion.replace(' ', ''):  # make sure the suggestion has exact same characters as error in the same order as error and without considering spaces
                error.replace(suggestion)
                break
    return checker.get_text()


def fix_row_spaces(inputmodel_rows, fix_columns,session):
    '''
    Take an input model row and fix possible missing spaces in model column.
    '''
    for inputmodel_row in inputmodel_rows:
        for model_column in fix_columns:
            line = getattr(inputmodel_row,model_column)
            line = fixline(line)
            setattr(inputmodel_row,model_column,line)
        session.commit()



def fixmodelSpaces(inputmodel):
    '''
    Gets all the database entries for the given model and goes though each one-off
    using the fixline function to put spaces back in to any fields called; notes,
    quotes or definition.
    '''
    target_columns = set(['definition','notes','quote'])
    model_all = inputmodel.query.all()
    model_all_ids = db.session.query(inputmodel.id).all()
    model_all_ids = [i[0] for i in model_all_ids]  # Strip tuples.  TODO do this nicer
    m0=model_all[0]
    model_attributes = set(dir(m0)) #all model rows have the same class attributes

    # columns we will try to fix missing spaces for.
    fix_columns = list(model_attributes.intersection(target_columns))

    if MUTLIP == True:

        cpus = range(0,mp.cpu_count()-1) #leave one cpu free.
        batchsize=1000
        chunks = [model_all_ids[x:x+batchsize] for x in xrange(0, len(model_all_ids),batchsize)]
        # chunks = deque(chunks)
        #Multiprocesses, note we do it this way as our functions aren't picklable
        # in this class, so using the sensible pool method won't work easily.
        remaining_chunks = True
        while remaining_chunks == True:
            jobs=[]
            sessions=[]
            engines=[]
            for cpu in cpus:
                #configure an engine and sessionamker. Each process needs its own session.
                engine = create_engine(ProdConfig.SQLALCHEMY_DATABASE_URI)
                Session = sessionmaker(bind=engine)
                engine.dispose() #Don't accidentally carry over
                session = Session()
                sessions.append(session)
                engines.append(engine)
                try:
                    sublist=chunks.pop()
                except IndexError as e:
                    print "all chunks underway"
                    remaining_chunks = False
                    break
                # Query the db using our session for all matching ids
                row_sublist = session.query(inputmodel).filter(inputmodel.id.in_(sublist)).all()
                p = mp.Process(target = fix_row_spaces, args=(row_sublist,fix_columns,session,))
                jobs.append(p)
                p.start()
            for job in jobs:
                job.join()
            for s in sessions:
                s.commit()
                s.close()
    else:
        for modeli in model_all:
            fix_row_spaces([modeli],fix_columns,db.session)
    db.session.commit() #commit changes to db

def insert_most_missingSpaces():
    '''
    Tries to add spaces to fields that might have concatination
    '''
    fixmodelSpaces(Headword)
    fixmodelSpaces(Citation)
    print "Most concatinations fixed"
