# -*- coding: utf-8 -*-

'''Helper functions for importing the nzdc database from the old server.'''

'''This file may be safely removed once all data pre-processing is completed'''

import subprocess
import datetime as dt
import fileinput

from DictionaryOfNewZealandEnglish.user.models import *
from DictionaryOfNewZealandEnglish.headword.models import *
from DictionaryOfNewZealandEnglish.headword.attribute.models import *
from DictionaryOfNewZealandEnglish.headword.citation.models import *



# TODO add a condition to immediately return nil if in production
def nzdc_resetdb():
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
def nzdc_seed():
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




# Processed data was missing various Notes found on the db
# this code should add those notes into the text files
# (which can then be uploaded using existing code).
def addNotesToDb(myfile):
    #print "here"
    head_loc = "./addDbNotes/Headwords_working_copy.txt" # tab delimited file from db
    file_loc = "./addDbNotes/db files Aug 2015/nzdc_export_"
    file_type = ".txt"
    action = myfile.split(":")

    myfile = action[0]
    print ""
    print "##################################################################"
    if myfile == "all":
      for myfile in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        print "#### Importing data from file: %s ##" % (file_loc + myfile + file_type)
        writeNotesTotextFile(file_loc, myfile, file_type, head_loc)
    else: 
      print "#### Importing data from file: %s ##" % (file_loc + myfile + file_type)
      writeNotesTotextFile(file_loc, myfile, file_type, head_loc)

    print "#### Copied Notes to %s.txt ..." % myfile


def writeNotesTotextFile(file_loc, myfile, file_type, head_loc):
    # Files are sets of word data including 0+ Citations
    # Word data starts with a headword and finishes with a blank line after all citations.
    # Citations data starts with "Citations"
    # A Citation starts with "Date: 18/04/2001" and finishes with "Notes: stuff"
    # next citation starts with blank line followed by "Date:"
    # next headword starts with blank line not followed by "Date:"

    # head_loc is Headword data from the db, including the Notes desired
    
    # input two files {nzdc_export_Q.txt, Headwords.txt}, output two files 
    # eg: {Q.txt, QHeadwords.txt} 
    #      Q.txt is headwords with notes attached
    #      QHeadwords has headwords that did not find a unique match

    ### NB: works on fresh file only. Running this a second time generates odd results.
    
    # ref: HeadwordID	Headword	HomonymNumberID	WordClassID	SenseNumberID	
    #      Definition	RegisterID	DomainID	RegionID	See	Pronunciation
    #      Notes	LastUpdateBy	EntryDate	LastUpdateDate	OriginID	Register2ID	archived

    with open(file_loc + myfile + file_type) as original:
     with open(head_loc) as dbHeadwords:
      #export = open("%s.txt" % myfile, "a")
      workToDo = open("addDbNotes/db files Aug 2015/%sHeadwords.txt" % myfile, "w")
      currentLine = nextLine = ""
      nextLineElements = []
      i = n = 1
      for line in dbHeadwords:
        if len(nextLineElements) == 1:
          currentLine = currentLine + nextLine
        else:
          currentLine = nextLine
        nextLine = line.strip()
        nextLineElements = nextLine.split('\t')
        if currentLine == "" or len(nextLineElements) == 1:
          continue

        # a line is typically (not always) a complete headword entry in tab-delimited string
        h = currentLine.split('\t')
        # is of interest
        if len(h) > 1 and len(h[1]) > 0 and h[1][0].capitalize() == myfile:
          # line is not empty
            # second element (headword) has substance
              # first letter of headword is of interest
          if len(h) >= 12 and len(h[11]) > 0:      
              # the notes element exists
                # notes element has content

            headword = h[1].strip()
            notes    = h[11].strip()
            print "### (1) Headword: %s, Notes: %s" % (headword, notes)

            # 1. is this headword unique? (first loop)
            unique = headword_is_unique( headword, myfile )

            # 2. if headword is unique, add notes into the file (second loop)
            if unique:
              # This loops through and re-writes the entire file to update a headword
              entry_found = False
              for myfile_line in fileinput.input("addDbNotes/db files Aug 2015/nzdc_export_%s.txt" % myfile, inplace = 1):
                r = ""
                # unique headword found
                if myfile_line.strip() == headword:
                  entry_found = True
                # find the first Notes entry
                if entry_found and myfile_line.strip() == "Notes:":
                  entry_found = False             
                  new_notes_line = "Notes: %s\n" % notes
                  #####
                  r = new_notes_line
                else:
                  #####
                  r = myfile_line.strip()
                print r

                #export.write(str(s)+"\n")
                #export.write(s+"\n")

              # most entries are contained on one line, replace with token
              workToDo.write("--//--\n")
            else:
              # un-actioned entries go here
              workToDo.write("\t".join(h) +"\n")
     


        i = i + 1
        # limits output for testing
#        print "### " + str(i)
#        if i >= 21:
#          break

      print "total entries: %d, \"%s\" entries: %d" %(i, myfile, n)


# Processed data was missing various Registers and Flags found on the db
# this code should add those notes into the text files
# (which can then be uploaded using existing code).
def addStuffToDb(myfile):  # python manage.py addStuff A:db  
    print "here"
    head_loc = "../addDbStuff/NZDCTEST_flag_words.txt" # tab delimited file from db
    file_loc = "../addDbStuff/db files Nov 2015/nzdc_export_"
    file_type = ".txt"
    action = myfile.split(":")

    myfile = action[0]
    print ""
    print "##################################################################"
    if myfile == "all":
      for myfile in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        print "#### Importing data from file: %s ##" % (file_loc + myfile + file_type)
        writeStuffTotextFile(file_loc, myfile, file_type, head_loc)
    else: 
      print "#### Importing data from file: %s ##" % (file_loc + myfile + file_type)
      writeStuffTotextFile(file_loc, myfile, file_type, head_loc)

    print "#### Copied Notes to %s.txt ..." % myfile


def writeStuffTotextFile(file_loc, myfile, file_type, head_loc):

    with open(file_loc + myfile + file_type) as original:
     with open(head_loc) as dbHeadwords:
      #export = open("%s.txt" % myfile, "a")
      workToDo = open("../addDbStuff/db files Nov 2015/%sHeadwords.txt" % myfile, "w")
      currentLine = nextLine = ""
      nextLineElements = []
      i = n = 1
      for line in dbHeadwords:
        # a line is a complete headword entry in tab-delimited string
        h = line.split('\t')
        # in case there are more tabs than expected (eg: in the definition text)
        not_broken = len(h)==3

        headword = h[0].strip()
        definition = h[1][0:20] # first 10 chars should be enough
        stuff    = h[2].strip()

        if headword[0].upper() == myfile.upper():
          print "### (1) Headword: %s, Stuff: %s" % (headword, stuff)

        # 1. is this headword unique? (first loop)
        unique = headword_is_unique( headword, definition, myfile )

        # 2. if headword is unique, add notes into the file (second loop)
        if unique and not_broken:
          # This loops through and re-writes the entire file to update a headword
          entry_found = False
          definition_found = False
          flag_found = False
          for myfile_line in fileinput.input("../addDbStuff/db files Nov 2015/nzdc_export_%s.txt" % myfile, inplace = 1):
            
            # headword found
            if myfile_line.strip() == headword:
              entry_found = True
            if myfile_line.split(':')[0] == "Definition" and myfile_line.split(':')[1][0:20] == definition:
              definition_found = True
            # find the first Flag entry
            if entry_found and definition_found and myfile_line.split(':')[0] == "Flag":
              flag_found = True          
              print "Flag: %s" % stuff

            # insert Flag entry if it does not exist
            elif entry_found and definition_found and not flag_found and myfile_line.split(':')[0] == "Domain":
              entry_found = False
              definition_found = False
              flag_found = False          
              print "Flag: %s" % stuff # insert Flag
              print myfile_line.strip()  # plus Domain

            else:
              print myfile_line.strip()

                #export.write(str(s)+"\n")
                #export.write(s+"\n")

          # most entries are contained on one line, replace with token
          workToDo.write("--//--\n")
        else:
          # un-actioned entries go here
          workToDo.write("\t".join(h) +"\n")
     


        i = i + 1
        # limits output for testing
#        print "### " + str(i)
#        if i >= 21:
#          break

      print "total entries: %d, \"%s\" entries: %d" %(i, myfile, n)


# definition is first 10 chars to the definition
def headword_is_unique(headword, definition, myfile):
      entry = False
      found = False
      unique = False
      with open("../addDbStuff/db files Nov 2015/nzdc_export_%s.txt" % myfile) as file_itr: ########
        for l in file_itr:
          line = l.strip()
          if line == "" or line == "Citations" or ':' in line:
            continue

          if line == headword:
            for l in file_itr:
              line = l.split(':') # looking for Definition:
              #print "HERE: %s", line[0]
              if line[0] == "Definition":
                if line[1][0:20] == definition: # check first 10 chars
                  if not found:
                    unique = True
                    found = True
                  else:
                    unique = False
                break
            # NB: prints once for every headword match
            #     False results may precede a True result, which may in turn be rendered False.
            print "#### (2) headword: %s, unique: %r" % (headword, unique)
      return unique
