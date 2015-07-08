#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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


### Part 1. Pre-processing ### 
# Convert rtf files into txt files to strip away formating info.
# Cut n paste contents into gedit. Check last listing matches.
# run python manage.py data_import A
# will process text file A.txt and print to terminal
# run python manage.py data_import all
# will process all 26 text files and print to terminal
### Part 2. Load db ###
# inserts "create entries" commands into the script
# run python manage.py data_import A:db
# will process text file A.txt, print to terminal and load data to db
@manager.command
def data_import(myfile):
    file_loc = "./db files June 2015/nzdc_export_"
    file_type = ".txt"
    load_db = False
    action = myfile.split(":")
    try:
      if action[1] == "db":
        load_db = True
        # prep database
        print "#### removing old files"
        subprocess.call(["rm", "dev.db"])
        subprocess.call(["rm", "-r", "migrations"])
        print "#### init db"
        subprocess.call(["python", "manage.py", "db", "init"])
        print "#### migrate db"
        subprocess.call(["python", "manage.py", "db", "migrate"])
        print "#### upgrade db"
        subprocess.call(["python", "manage.py", "db", "upgrade"])
        
        # load first users
        initial_db_users()
        # load secondary tables
        seed_tables()
    except:
      # do nothing, try fails if action[1] does not exist, so load_db stays False
      print "Not changing database."

    myfile = action[0]
    print ""
    print "##################################################################"
    if myfile == "all":
      for myfile in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        print "#### Importing data from file: %s ##" % (file_loc + myfile + file_type)
        data_import_read_files(file_loc, myfile, file_type, load_db)
    else: 
      print "#### Importing data from file: %s ##" % (file_loc + myfile + file_type)
      data_import_read_files(file_loc, myfile, file_type, load_db)

    if load_db:
      print "#### Loaded database ...???"

def data_import_read_files(file_loc, myfile, file_type, load_db):
    # Files are sets of word data including 0+ Citations
    # Word data starts with a headword and finishes with a blank line after all citations.
    # Citations data starts with "Citations"
    # A Citation starts with "Date: 18/04/2001" and finishes with "Notes: stuff"
    # next citation starts with blank line followed by "Date:"
    # next headword starts with blank line not followed by "Date:"
    with open(file_loc + myfile + file_type) as text:
      currentLine = nextLine = ""
      i = 1
      for line in text:
        currentLine = nextLine
        nextLine = line.strip()
        if currentLine == "":
          continue

        # this is a headword
        currentLine, nextLine, headword, headword_obj = create_headword(currentLine, nextLine, text, i)

        # this is zero or more citations for the headword
        nextLine, headword = create_citation_list(currentLine, 
                                                  nextLine, 
                                                  text, 
                                                  headword,
                                                  headword_obj)
        if nextLine == None:
          break
        i = i + 1
        # limits output for testing
#        print "### " + str(i)
#        if i >= 21:
#          break

def create_headword(currentLine, nextLine, text, counter):
    seed_date = dt.datetime.utcnow()
    headword = {"Headword": currentLine}
    headword["Headword_id"] = counter
    print "%d %s" % (counter, headword["Headword"])
    print "%d %s," % (counter, headword["Headword"]),
    print "{k: v} Headword_id: %s " % (headword["Headword_id"])

    ###########################################################################
    # hashes of secondary table ids
    data_set={'none': 0, 'Orsman': 1, 'DNZE': 2, 'Incomings': 0}

    word_class={'none': 0, '[none]': 0, '[_none_]': 69, 'abbreviation': 39, 'adjective': 12, 'adverb': 17, 'conjunction': 27, 'determiner': 71, 'exclamation': 23, 'noun': 1, 'phrase': 9, 'prefix': 73, 'preposition': 30, 'pronoun': 8, 'verb': 13}

    origin={'': 2, 'none': 2, '[none]': 2, 'abbreviation': 18, 'Aboriginal': 10, 'acronym': 8, 'blend': 19, 'British dialect': 11, 'catchphrase': 12, 'ellipsis': 17, 'eponym': 22, 'euphemism': 15, 'expletive': 16, 'initialism': 14, 'Maori': 4, 'Moriori': 21, 'Polynesian': 7, 'rhyming slang': 9, 'Samoan': 5, 'Tongan': 6, 'toponym':23}

    domain={'': 1, 'none': 1, '[none]': 1, 'Commerce': 16, 'Cuisine': 4, 'Environment': 8, 'Geology': 5, 'Marine': 12, 'Media': 20, 'Politics': 27, 'Rural': 3, 'Science': 26, 'Sport': 6}

    region={'': 1, 'none': 1, '[none]': 1, 'New Zealand and Australia': 3, 'New Zealand & Australia': 3, 'New Zealand (Southern South Island)': 7, 'New Zealand (West Coast South Island)': 8, 'New Zealand and Pacific': 9}

    sense_number={'': 1, '1': 2, '2': 25, '3': 37, '4': 48, '5': 59, '6': 70, '7':80, '8': 91, '9': 101}

    homonym_number={'': 1, '1': 11, '2': 18, '3': 19, '4': 20, '5': 22, '6': 23, '7':24, '8': 25, '9': 26}
    ###########################################################################

    # Definitions may be over multiple lines
    do_definition = False
    definition_text = ""

    for line in text:
      currentLine = nextLine
      nextLine = line.strip()

      # roll past empty lines
      if currentLine == "":
        if nextLine == "":
          # roll past empty lines
          continue
        if nextLine[:7] == "Origin:" or nextLine[:6] == "Notes:":
          # roll nextLine to currentLine
          continue

      # headword data
      splt = currentLine.split(':', 1)
      if splt[0] == "Definition":
        # start definition, which may be multi-lines
        do_definition = True
      if do_definition:
        if splt[0] == "Definition":
          definition_text = splt[1]
        elif splt[0] != "Origin":
          definition_text = definition_text + " " + currentLine
        if splt[0] == "Origin":
          # collecting definition is finished
          headword["Definition"] = definition_text
          print "%d %s," % (counter, headword["Headword"]),
          print "{k: v} %s: %s " % ("Definition", headword["Definition"])
          do_definition = False

      if not do_definition:
        if currentLine == "":
          continue
        headword[splt[0]] = splt[1]
        print "%d %s," % (counter, headword["Headword"]),
        print "{k: v} %s: %s " % (splt[0], headword[splt[0]])
      if nextLine == "Citations":
        break
    
    #### loop finished
    #### groom data
    definition = headword["Definition"]
    if definition == "":
      definition = ""
    # data_set = {DNZE, Orsman, Incomings}
    data_set_id = 0 # data not in suplied data

    # create database entry
    headword_obj = Headword.create(
                 headword=headword["Headword"],
                 definition=definition,
                 see=headword["See"],
                 pronunciation=headword["Pronunciation"],
                 notes=headword["Notes"],
                 data_set_id=data_set_id,
                 homonym_number_id=homonym_number[headword["Homonym Number"].strip()], 

                 word_class_id=word_class[headword["Word Class"].strip()],
                 sense_number_id=sense_number[headword["Sense Number"].strip()], 

                 origin_id=origin[headword["Origin"].strip()], 
                 #register_id=16, 
                 domain_id=domain[headword["Domain"].strip()], 
                 region_id=region[headword["Region"].strip()], 
                 updated_at=seed_date,
                 updated_by="admin"
                   )
    
    return currentLine, nextLine, headword, headword_obj

def create_citation_list(currentLine, nextLine, text, headword, headword_obj):
    citation_count = 0
    for line in text:
#      print "### currentLine " + currentLine
#      print "### nextLine " + nextLine
#      print "#### list line => " + line
      if nextLine == "Citations":
        # roll nextLine to "Date:"
        currentLine = nextLine
        nextLine = line.strip()
        if nextLine == None:
          # end of file
          return None, headword
        if nextLine[:5] != "Date:":
          # zero citations for this headword
          print ""
          return nextLine, headword
        continue
      if currentLine == "Citations" or nextLine[:5] == "Date:":
        # roll "Date:" to currentLine
        currentLine = nextLine
        nextLine = line.strip()
        #continue

      citation_count = citation_count + 1
      currentLine, nextLine, headword = create_citation(currentLine, 
                                                        nextLine, 
                                                        text, 
                                                        citation_count, 
                                                        headword,
                                                        headword_obj)

      if nextLine[:5] != "Date:":
        # citations finished
        print ""
        return nextLine, headword


def create_citation(currentLine, nextLine, text, citation_count, headword, headword_obj):
    seed_date = dt.datetime.utcnow()
    citation = {"Citation_id": citation_count}
    splt = currentLine.split(':', 1)
    citation["Date"] = splt[1]
    print ""
    print "%d %s, Citations " % (headword["Headword_id"], headword["Headword"])
    print "%d-%d, {k: v} Citation_id: %s " % (headword["Headword_id"], citation_count, citation["Citation_id"])
    print "%d-%d, {k: v} Date: %s " % (headword["Headword_id"], citation_count, citation["Date"])

    # Quotes may be over multiple lines
    do_quote = False
    quote_text = ""
    end_of_citation = False
    
    for line in text:
#      print "### line => " + line
#      print "### currentLine " + currentLine
#      print "### nextLine " + nextLine
      currentLine = nextLine
      nextLine = line.strip()

      # blank line is end of citation
      if currentLine == "":
        if nextLine == "" or do_quote:
          # roll past empty lines
          continue
        if (nextLine[:6] == "Notes:" or 
           nextLine[:6] == "Quote:" or 
           nextLine[:11] == "Vol / Page:" or 
           nextLine[:8] == "Edition:"):
          # roll nextLine to currentLine
          continue

      if end_of_citation:
        # add citation to Headword hash
        headword["citation_%d" % citation_count] = citation
        # add citation to db
        add_citation_to_headWord(citation, headword_obj)
        return currentLine, nextLine, headword

      if currentLine[:6] == "Notes:":
        end_of_citation = True

      # citation data
      splt = currentLine.split(':', 1)
      if splt[0] == "Quote":
        quote_text = ""
        do_quote = True

      if do_quote:
        if splt[0] == "Quote":
          quote_text = splt[1]
        elif splt[0] != "Notes":
          quote_text = quote_text + " " + currentLine
        # collecting quote is finished
        if splt[0] == "Notes":
          citation["Quote"] = quote_text
          print "%d-%d, {k, v} %s: %s " % (
            headword["Headword_id"], citation_count, "Quote", citation["Quote"])
          do_quote = False
      
      if not do_quote:
        if currentLine == "":
          continue
        citation[splt[0]] = splt[1]
        print "%d-%d, {k, v} %s: %s " % (
          headword["Headword_id"], citation_count, splt[0], citation[splt[0]])
      
    else:
      citation[splt[0]] = splt[1]
      print "%d-%d, {k, v} %s: %s " % (
         headword["Headword_id"], citation_count, splt[0], citation[splt[0]])

      # add last citation to Headword hash
      headword["citation_%d" % citation_count] = citation
      # add citation to db
      add_citation_to_headWord(citation, headword_obj)

      currentLine = nextLine
      return currentLine, nextLine, headword

def add_citation_to_headWord(citation, headword_obj):
    seed_date = dt.datetime.utcnow()
    circa = 0
    # prep citation hash info
    d,m,y = citation["Date"].split("/")
    if int(d) < 1:
      d = '1'
      circa = 1
    if int(m) < 1:
      d = '1'
      m = '1'
      circa = 1
    date = dt.datetime(int(y), int(m), int(d))

    citation_obj = Citation.create(
                 date       = date,
                 circa      = circa,
                 author     = citation["Author"].strip(),
                 source_id  = get_source_id(citation),
                 vol_page   = citation["Vol / Page"].strip(),
                 edition    = citation["Edition"].strip(),
                 quote      = citation["Quote"].strip(),
                 notes      = citation["Notes"].strip(),
                 archived   = False,
                 updated_at = seed_date,
                 updated_by = "admin"
                   )
    headword_obj.citations.append(citation_obj)

def get_source_id(citation):
    seed_date = dt.datetime.utcnow()
    source = citation["Source"].strip()
    source_obj = Source.query.filter_by(name=source).first()
    if source_obj:
      return source_obj.id

    source_obj = Source.create(
                 name=source,
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    return source_obj.id


def initial_db_users():
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


# TODO add a condition to immediately return nil if in production
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
    initial_db_users()
    seed_tables()

    seed_date = dt.datetime.utcnow()
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
                 updated_by="admin"
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
                 updated_by="admin"
                   )

    Headword.create(
                 headword="Cheddar cheese",
                 definition="yellow cheese found in lunchboxes",
                 see="Ches n' Dale",
                 pronunciation="cheda",
                 notes="often swapped for raisens",
                 data_set_id=3,
                 homonym_number_id=20, 
                 word_class_id=27,
                 sense_number_id=59, 
                 origin_id=16, 
                 #register_id=16, 
                 domain_id=26, 
                 region_id=7, 
                 updated_at=seed_date,
                 updated_by="admin"
                   )

    Headword.create(
                 headword="Ches n' Dale",
                 definition="Makers of hand crafted yellow cheese found in lunchboxes",
                 see="Cheddar cheese",
                 pronunciation="cheda",
                 notes="comes in foil wrapped segments",
                 data_set_id=3,
                 homonym_number_id=20, 
                 word_class_id=27,
                 sense_number_id=59, 
                 origin_id=16, 
                 #register_id=16, 
                 domain_id=26, 
                 region_id=7, 
                 updated_at=seed_date,
                 updated_by="admin"
                   )

    Citation.create(
                 day = 1, month = 1, year = 1972,
                 circa      = 0,
                 author     = "Matt",
                 source_id  = 1,
                 vol_page   = "1/253",
                 edition    = "5",
                 quote      = "The amber elixer of life",
                 notes      = "Beer",
                 archived   = False,
                 updated_at = seed_date,
                 updated_by = "admin"
                   )

    Citation.create(
                 day = 1, month = 2, year = 1972,
                 circa      = 0,
                 author     = "Colonel Dagg",
                 source_id  = 2,
                 vol_page   = "",
                 edition    = "",
                 quote      = "Love the smell of napalm in the morning.",
                 notes      = "",
                 archived   = False,
                 updated_at = seed_date,
                 updated_by = "admin"
                   )

    Citation.create(
                 day = 1, month = 2, year = 1972,
                 circa      = 0,
                 author     = "Mr Flintstone",
                 source_id  = 3,
                 vol_page   = "",
                 edition    = "",
                 quote      = "The Mesianic era hit rock bottom.",
                 notes      = "",
                 archived   = False,
                 updated_at = seed_date,
                 updated_by = "admin"
                   )

    Citation.create(
                 day = 1, month = 2, year = 1984,
                 circa      = 0,
                 author     = "Ches n' Dale",
                 source_id  = 4,
                 vol_page   = "",
                 edition    = "",
                 quote      = "We really know our cheese!",
                 notes      = "The boys from down on the farm.",
                 archived   = False,
                 updated_at = seed_date,
                 updated_by = "admin"
                   )
    
    h = Headword.query.get(1)
    h.citations.append(Citation.query.get(1))
    h.citations.append(Citation.query.get(2))
    h = Headword.query.get(3)
    h.citations.append(Citation.query.get(4))

    h = Headword.query.get(1)
    h.flags.append(Flag.query.get(1))
    h.flags.append(Flag.query.get(4))
    h = Headword.query.get(2)
    h.flags.append(Flag.query.get(1))

    h = Headword.query.get(1)
    h.registers.append(Register.query.get(12))
    h.registers.append(Register.query.get(16))
    h = Headword.query.get(2)
    h.registers.append(Register.query.get(13))



def seed_tables():
    seed_date = dt.datetime.utcnow()

    Homonym_number.create( id=1,
                 name="0",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Homonym_number.create( id=11,
                 name="1",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Homonym_number.create( id=18,
                 name="2",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Homonym_number.create( id=19,
                 name="3",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Homonym_number.create( id=20,
                 name="4",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Homonym_number.create( id=22,
                 name="5",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Homonym_number.create( id=23,
                 name="6",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Homonym_number.create( id=24,
                 name="7",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Homonym_number.create( id=25,
                 name="8",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Homonym_number.create( id=26,
                 name="9",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")


    Word_class.create( id=0,
                 name="none",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=69,
                 name="[_none_]",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=39,
                 name="abbreviation",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=12,
                 name="adjective",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=17,
                 name="adverb",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=27,
                 name="conjunction",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=71,
                 name="determiner",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=23,
                 name="exclamation",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=1,
                 name="noun",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=9,
                 name="phrase",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=73,
                 name="prefix",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=30,
                 name="preposition",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=8,
                 name="pronoun",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Word_class.create( id=13,
                 name="verb",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")

    Sense_number.create( id=1,
                 name="none",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Sense_number.create( id=2,
                 name="1",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Sense_number.create( id=25,
                 name="2",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Sense_number.create( id=37,
                 name="3",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Sense_number.create( id=48,
                 name="4",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Sense_number.create( id=59,
                 name="5",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Sense_number.create( id=70,
                 name="6",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Sense_number.create( id=80,
                 name="7",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Sense_number.create( id=91,
                 name="8",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Sense_number.create( id=101,
                 name="9",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")

    Register.create( id=1,
                 name="none",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=19,
                 name="archaic",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=16,
                 name="corse slang",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=9,
                 name="dated",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=11,
                 name="derogatory",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=15,
                 name="ephemistic",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=4,
                 name="formal",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=6,
                 name="historical",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=14,
                 name="humorous",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=5,
                 name="informal",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=12,
                 name="literary",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=20,
                 name="obsolete",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=7,
                 name="offensive",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=13,
                 name="rare",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Register.create( id=17,
                 name="trademark",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")

    Domain.create( id=1,
                 name="none",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Domain.create( id=16,
                 name="Commerce",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Domain.create( id=4,
                 name="Cuisine",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Domain.create( id=8,
                 name="Environment",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Domain.create( id=5,
                 name="Geology",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Domain.create( id=12,
                 name="Marine",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Domain.create( id=20,
                 name="Media",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Domain.create( id=27,
                 name="Politics",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Domain.create( id=3,
                 name="Rural",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Domain.create( id=26,
                 name="Science",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Domain.create( id=6,
                 name="Sport",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")

    Flag.create( id=0,
                 name="none",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Flag.create( id=1,
                 name="Transport",
                 notes="DB",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Flag.create( id=2,
                 name="Slang",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Flag.create( id=3,
                 name="Farm Words",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Flag.create( id=4,
                 name="Geology",
                 notes="Geology",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")

    Region.create( id=1,
                 name="none",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Region.create( id=3,
                 name="New Zealand and Australia",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Region.create( id=7,
                 name="New Zealand (Southern South Island)",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Region.create( id=8,
                 name="New Zealand (West Coast South Island)",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Region.create( id=9,
                 name="New Zealand and Pacific",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")

    Origin.create( id=2,
                 name="none",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=18,
                 name="abbreviation",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=10,
                 name="Aboriginal",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=8,
                 name="acronym",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=19,
                 name="blend",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=11,
                 name="British dialect",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=12,
                 name="catchphrase",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=17,
                 name="ellipsis",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=22,
                 name="eponym",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=15,
                 name="euphemism",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=16,
                 name="expletive",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=14,
                 name="initialism",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=4,
                 name="Maori",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=21,
                 name="Moriori",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=7,
                 name="Polynesian",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=9,
                 name="rhyming slang",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=5,
                 name="Samoan",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=6,
                 name="Tongan",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Origin.create( id=23,
                 name="toponym",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")

    Data_set.create( id=0,
                 name="none",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Data_set.create( id=1,
                 name="Orsman",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Data_set.create( id=2,
                 name="DNZE",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Data_set.create( id=3,
                 name="Incomings",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
'''
    Source.create( id=0,
                 name="none",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Source.create( id=1,
                 name="NZ TV Times",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Source.create( id=2,
                 name="Wellington Craft Beers Monthly",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Source.create( id=3,
                 name="On the Search for Dragons",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
    Source.create( id=4,
                 name="TVNZ Advertising",
                 notes="",
                 archived=False,
                 updated_at=seed_date,
                 updated_by="admin")
'''

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
