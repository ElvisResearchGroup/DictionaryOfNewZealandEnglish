# -*- coding: utf-8 -*-

'''Helper functions for importing the nzdc database from the old server.'''

'''This file may be safely removed once all data pre-processing is completed'''

import subprocess
import datetime as dt

from DictionaryOfNewZealandEnglish.user.models import *
from DictionaryOfNewZealandEnglish.headword.models import *
from DictionaryOfNewZealandEnglish.headword.attribute.models import *
from DictionaryOfNewZealandEnglish.headword.citation.models import *





# Processed data was missing various Notes found on the db
# this code should add those notes into the text files
# (which can then be uploaded using existing code).
@manager.command
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


def headword_is_unique(headword, myfile):
      entry = False
      found = False
      unique = False
      for l in open("addDbNotes/db files Aug 2015/nzdc_export_%s.txt" % myfile): ########
        line = l.strip()
        if line == "" or line == "Citations" or ':' in line:
          continue
        if line == headword:
          if not found:
            unique = True
            found = True
          else:
            unique = False
          print "#### (2) headword: %s, unique: %r\n" % (headword, unique)
      return unique
