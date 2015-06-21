# -*- coding: utf-8 -*-
# Citations

from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session, g)
from flask.ext.login import login_required, current_user
from flask_wtf import Form
import DictionaryOfNewZealandEnglish.utils as utils
import logging, sys, re
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
    if not current_user.is_admin:
        return redirect(url_for('public.home'))

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
    if not current_user.is_admin:
        return redirect(url_for('public.home'))

    headword = request.args.get('headword')
    form = CitationForm(request.form)
    return render_template("headwords/citations/new.html", form=form,
                                                           headword=headword)


@blueprint.route("/create", methods=["POST"])
@login_required
def create():
    if not current_user.is_admin:
        return redirect(url_for('public.home'))

    form = CitationForm(request.form)
    headword = request.args.get('headword')

    try:
        cit_obj = __create_citation(form, headword)

        circa = ""
        if form.circa.data:
          circa = "circa "
        form_date = __form_date(form)
        date = "{0}/{1}/{2}".format(form_date[0], 
                                        form_date[1], 
                                        form_date[2])
        flash("New citation created: {0} ({1}{2})".format(form.author.data,
                                                   circa, 
                                                   date, 'success'))
    
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
    if not current_user.is_admin:
        return redirect(url_for('public.home'))

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
    date = __form_date(form)
    citation = Citation.create(
                 day = int(date[0]), month = int(date[1]), year = int(date[2]),
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
    date = re.split(r'[/,\s]\s*', form.date.data)
    #date = dt.datetime(int(form_date[2]), int(form_date[1]), int(form_date[0]))
    return date


def __set_data_for_citation(citation_id, form):
    db_row = Citation.query.get(citation_id)

    try:
      date = __form_date(form)
      Citation.update(db_row,
                 day = int(date[0]), month = int(date[1]), year = int(date[2]),
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


