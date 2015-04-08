# -*- coding: utf-8 -*-
#from flask import Blueprint, render_template
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session, g)
from flask.ext.login import login_required, current_user
from flask_wtf import Form
import DictionaryOfNewZealandEnglish.utils as utils
import logging
import sys
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from DictionaryOfNewZealandEnglish.database import db
from DictionaryOfNewZealandEnglish.headword.citation.forms import *
from DictionaryOfNewZealandEnglish.public.forms import LoginForm
from DictionaryOfNewZealandEnglish.headword.citation.models import *
from DictionaryOfNewZealandEnglish.database import engine
import datetime as dt
import re
from operator import itemgetter

blueprint = Blueprint("citations", __name__, url_prefix='/headwords/citations',
                        static_folder="../static")


@blueprint.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    headword = request.args.get('headword')
    citation_id = request.args.get('citation_id')
    citation = Citation.query.get(citation_id)
    form = CitationForm(request.form, obj=citation)
    if request.method == "GET":
      return render_template("headwords/citations/edit.html", form=form,
                                                              citation_id=citation_id,
                                                              headword=headword)
    if request.method == "POST":
      data = __set_data_for_citation(citation_id, form)
      return render_template("headwords/citations/edit.html", form=form,
                                                              citation_id=citation_id,
                                                              headword=headword)

@blueprint.route("/new", methods=["GET"])
@login_required
def new():
    headword = request.args.get('headword')
    form = CitationForm(request.form)
    return render_template("headwords/citations/new.html", form=form,
                                                           headword=headword)


@blueprint.route("/create", methods=["POST"])
@login_required
def create():
    form = CitationForm(request.form)
    headword = request.args.get('headword')    
    if form.validate():
      # TODO add validations
      flash('Validations are turned off.')
    else:
      # TODO detail errors
      flash('There is an error.')
      return render_template("headwords/citations/new.html", form=form,
                                                             headword=headword)
    try:
        cit_obj = __create_citation(form, headword)

        circa = ""
        if form.circa.data:
          circa = "circa "
        flash("New citation created: {0} ({1}{2})".format(form.author.data,
                                                   circa, 
                                                   __form_date(form)), 'success')
    
        return render_template("headwords/citations/edit.html", 
                                                       form=form,
                                                       citation_id = cit_obj.id,
                                                       headword=headword)
    except (IntegrityError) as e:
        db.session.rollback()
        flash("Input error %s" % e)
        return render_template("headwords/citations/new.html", form=form, 
                                                              headword=headword)


@blueprint.route("/delete", methods=["GET"])
@login_required
def delete():
    citation_id = request.args.get('citation_id')
    headword    = request.args.get('headword')
    citation    = Citation.query.get(citation_id)
    headword    = Headword.query.filter_by(headword=headword).first()
    if citation in headword.citations:
      headword.citations.remove(citation)
      db.session.add(headword)
      db.session.commit()

    citations = headword.citations
    return render_template("headwords/show.html", headword=headword,
                                                  citations=citations)
    



#############################################################################
### Private

def __create_citation(form, headword):
    citation = Citation.create(
                            date       = __form_date(form),
                            circa      = form.circa.data,
                            author     = form.author.data,
                            source_id  = form.source.data.id,
                            vol_page   = form.vol_page.data,
                            edition    = form.edition.data,
                            quote      = form.quote.data,
                            notes      = form.notes.data,
                            archived   = False,
                            updated_at = dt.datetime.utcnow(),
                            updated_by = current_user.username    
                           )
    
    h = Headword.query.filter_by(headword=headword).first()
    h.citations.append(citation)
    db.session.add(h)
    db.session.commit()

    return citation


def __form_date(form):
    date = form.date.data
    return date


def __set_data_for_citation(citation_id, form):
    db_row = Citation.query.get(citation_id)

    try:
      Citation.update(db_row,
                        date       = __form_date(form),
                        circa      = form.circa.data,
                        author     = form.author.data,
                        source_id  = form.source.data.id,
                        vol_page   = form.vol_page.data,
                        edition    = form.edition.data,
                        quote      = form.quote.data,
                        notes      = form.notes.data,
                        archived   = form.archived.data,
                        updated_at = dt.datetime.utcnow(),
                        updated_by = current_user.username    
                       )
      flash("Edit of citation is saved.", 'success')
      return True
    except (IntegrityError, InvalidRequestError):
      db.session.rollback()
      flash("Edit of citation failed.", 'warning')
      return False


