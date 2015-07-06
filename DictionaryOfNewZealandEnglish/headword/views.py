# -*- coding: utf-8 -*-
# headwords
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session, g)
from flask.ext.login import login_required, current_user
from flask_wtf import Form
import DictionaryOfNewZealandEnglish.utils as utils
import logging
import sys
import string
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy import func
from DictionaryOfNewZealandEnglish.database import db
from DictionaryOfNewZealandEnglish.headword.forms import *
from DictionaryOfNewZealandEnglish.headword.models import *
from DictionaryOfNewZealandEnglish.headword.citation.models import *
import datetime as dt

blueprint = Blueprint("headword", __name__, url_prefix='/headwords',
                        static_folder="../static")


@blueprint.route("/index", methods=["GET"])
@login_required
def index():
    if request.args.get('letter'):
        headwords = []
        attribute_name = attribute_table = attribute_id = ""
        if request.args.get('letter') == 'attribute':
            attribute_table = request.args.get('table')
            attribute_name  = request.args.get('name')
            attribute_id  = request.args.get('name_id')

            if attribute_table == "Register":
              register = Register.query.filter_by(name=attribute_name).first()
              headwords = register.headwords              
            elif attribute_table == "Flag":
              flag = Flag.query.filter_by(name=attribute_name).first()
              headwords = flag.headwords         
            elif attribute_table == "Source":
              source = Source.query.filter_by(name=attribute_name).first()
              citations = source.citations
              for citation in citations:
                headwords = headwords + citation.headwords
            else:
              attr_id_label = attribute_table.replace(' ', '_').lower()+"_id"
              headwords = Headword.query.filter(
                                  getattr(Headword, attr_id_label) == attribute_id)
            title = "Words for {1}, {0}".format(attribute_name, attribute_table)
        else:
            letter = request.args.get('letter')
            headwords = Headword.query.filter(
                                  Headword.headword.startswith(letter)).all()
            title = "All words"

        counts = {}
        for letter in string.ascii_uppercase:
            counts[letter] = Headword.query.filter(Headword.headword.startswith(letter)).count()

        return render_template("headwords/index.html", letter=request.args.get('letter'),
                                                       title=title,
                                                       attribute_name=attribute_name,
                                                       attribute_table=attribute_table,
                                                       counts=counts,
                                                       #headword=headwords.first(),
                                                       headwords=headwords)

    # logged in users arrive here
    form = SearchForm(request.form, "search_data")
    return render_template("headwords/index.html", form=form)


@blueprint.route("/show", methods=["GET","POST"])
@login_required
def show():
    headword = headwords = None
    if request.method == "GET":
      # is passed headword_id as headword names are not unique 
      headword = Headword.query.get( request.args.get('headword_id') )
      output = 'sample_citations'
      if request.args.get('output'):
        output = request.args.get('output')
      
    if request.method == "POST":
      # uses headword name
      headword = request.form['headword']
      output  = request.form['output']
      # case insensitive search
      headwords = Headword.query.filter(func.lower(Headword.headword)==func.lower(headword)) 
      headword = headwords.first()
      # if more than one result, show a list with definitions
      if headwords.count() > 1:
        output = "definition_only"

    if headword == None:
      return redirect("headwords/index")

    more_citations = False
    citations = []
    if   output == 'all_citations':
      citations = headword.citations
    elif output == 'sample_citations':
      # Python InstrumentedList objects do not have a size function
      size = 0 
      for c in headword.citations:
        size = size + 1

      if size > 0:
        citations.append( headword.citations[0] )
      if size > 1:
        citations.append( headword.citations[-1] )
      if size > 2: # sample citations return only two citations
        more_citations = True

    return render_template("headwords/show.html", headword=headword,
                                                  headwords=headwords,
                                                  output=output,
                                                  citations=citations,
                                                  more_citations=more_citations)


@blueprint.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if not current_user.is_admin:
        return redirect(url_for('public.home'))
    headword = Headword.query.get( request.args.get('headword_id') )
    form = HeadwordForm(request.form, obj=headword)

    if request.method == "POST" and form.validate():
      data = __set_data_for_headword(headword, form)
      flash("Edit of %s is saved." % data.headword, 'success')
      
    return render_template("headwords/edit.html", 
                            form=form, 
                            headword=headword,
                            HeadwordForm=HeadwordForm)


@blueprint.route("/new", methods=["GET"])
@login_required
def new():
    if not current_user.is_admin:
        return redirect(url_for('public.home'))

    form = HeadwordForm(request.form)
    return render_template("headwords/new.html", form=form)


@blueprint.route("/create", methods=["POST"])
@login_required
def create():
    if not current_user.is_admin:
        return redirect(url_for('public.home'))

    form = HeadwordForm(request.form)
    if form.validate():
      headword = Headword.query.get( __create_headword(form) )
      flash("New headword created: %s" % form.headword.data, 'success')
      return render_template("headwords/show.html", form=form, headword=headword)
    
    flash('There is an error')
    return render_template("headwords/new.html", form=form)


#############################################################################
### Private

def __create_headword(form):
        h = Headword.create(
                        headword          = form.headword.data,
                        definition        = form.definition.data,
                        see               = form.see.data,
                        pronunciation     = form.pronunciation.data,
                        notes             = form.notes.data,
                        data_set_id       = __set_None_or(form.data_set.data),
                        homonym_number_id = __set_None_or(form.homonym_number.data), 
                        word_class_id     = __set_None_or(form.word_class.data), 
                        sense_number_id   = __set_None_or(form.sense_number.data), 
                        origin_id         = __set_None_or(form.origin.data),
                        domain_id         = __set_None_or(form.domain.data), 
                        region_id         = __set_None_or(form.region.data), 
                        updated_at        = dt.datetime.utcnow(),
                        updated_by        = current_user.username    )

        __set_join_tables(h, form)

        return h.id

def __set_None_or(data):
    if data == None:
      return None
    return data.id

def __set_data_for_headword(headword, form):
    try:
        h = Headword.update(headword,
                        headword          = form.headword.data,
                        definition        = form.definition.data,
                        see               = form.see.data,
                        pronunciation     = form.pronunciation.data,
                        notes             = form.notes.data,
                        data_set_id       = __set_None_or(form.data_set.data),
                        homonym_number_id = __set_None_or(form.homonym_number.data), 
                        word_class_id     = __set_None_or(form.word_class.data), 
                        sense_number_id   = __set_None_or(form.sense_number.data), 
                        origin_id         = __set_None_or(form.origin.data),
                        domain_id         = __set_None_or(form.domain.data), 
                        region_id         = __set_None_or(form.region.data), 
                        updated_at        = dt.datetime.utcnow(),
                        updated_by        = current_user.username, 
                        archived          = form.archived.data      )

        __set_join_tables(h, form)

    except (IntegrityError, InvalidRequestError):
        db.session.rollback()
        return "Database integrety constraint - %s already exists in the database" % form.headword.data

    return Headword.query.filter_by(headword=form.headword.data).first()


def __set_join_tables(headword, form):
        if form.register.data != None:
          register = form.register.data.name
          register = Register.query.filter_by(name=register).first()
          if register not in headword.registers and register.name != "[none]":
              headword.registers.append(register)
              db.session.add(headword)
              db.session.commit()

        if form.flag.data != None:
          flag = form.flag.data.name
          flag = Flag.query.filter_by(name=flag).first()
          if flag not in headword.flags and flag.name != "[none]":
              headword.flags.append(flag)
              db.session.add(headword)
              db.session.commit()


