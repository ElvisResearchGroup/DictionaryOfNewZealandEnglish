# -*- coding: utf-8 -*-
#from flask import Blueprint, render_template
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required
from flask_wtf import Form

from DictionaryOfNewZealandEnglish.user.forms import HeadwordForm
from DictionaryOfNewZealandEnglish.user.forms import RegisterForm
from DictionaryOfNewZealandEnglish.public.forms import LoginForm
from DictionaryOfNewZealandEnglish.user.models import Headword
from DictionaryOfNewZealandEnglish.user.models import Citation
from DictionaryOfNewZealandEnglish.database import engine
import datetime as dt

blueprint = Blueprint("user", __name__, url_prefix='/users',
                        static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    return render_template("users/members.html")



@blueprint.route("/insert", methods=["GET"]) #, "POST"])
def insert():
    user_form = LoginForm(request.form)
    form = HeadwordForm(request.form)
    return render_template("users/insert.html", form=form)




@blueprint.route("/insert", methods=["POST"])
def insertdb():
    
    user_form = LoginForm(request.form)
    form = HeadwordForm(request.form)
    if form.validate():
      flash('Inserting data, in theory - still working on this. Validations are turned off.')
    else:
      flash('Inserting data, in theory - still working on this. Validate == FALSE ')


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

#    date_obj = datetime.datetime.strptime(form.date.data, '%d/%m/%Y').date()

    homonym_number_id = 1
    word_class_id = 1
    sense_number_id = 1
    origin_id= 1
    register_id =1
    domain_id = 1
    region_id = 1
    #headword_citation = [1]
    #headword_flag = [1]
    updated_by = 1
    headword = Headword.create(headword = form.headword.data,
                               definition = form.definition.data,
                               see = form.see.data,
                               pronunciation = form.pronunciation.data,
                               notes = form.notes.data,
                               archived = form.archived.data,
                               data_set_id = form.data_set_id.data,

                               homonym_number_id=homonym_number_id, 
                               word_class_id=word_class_id, 
                               sense_number_id=sense_number_id, 
                               origin_id=origin_id, 
                               register_id=register_id, 
                               domain_id=domain_id, 
                               region_id=region_id, 
                               #headword_citation=headword_citation, 
                               #headword_flag=headword_flag, 
                               updated_at=dt.datetime.utcnow(),
                               updated_by=updated_by )

    return render_template("users/insert.html", form=form)





@blueprint.route("/search/", methods=["GET"])
@login_required
def search():
    # logged in users arrive here
    form = DataForm(request.form, "search_data")
    return render_template("users/search.html", form=form)


@blueprint.route("/search/db", methods=["POST"])
def searchdb():
    form = DataForm(request.form, "display_data")
    # Handle search
    if form.validate_on_submit():
        author = form.author.data
        source = form.source.data
        try:
            date = datetime.datetime.strptime(form.date.data, '%d/%m/%Y').date()
        except ValueError:
            date = ""

        citations = Citation.query.filter_by(author="Wallace", source="maximum").all()
        #citations = engine.execute('select * from Citations where author = :1', [author]).first()

        flash('Search form is validated ' + citations[0].source)

    else:
        flash_errors(form)

    #flash('Searching data - this page should display responses, but doesn\'t yet.')
    return render_template("users/search.html", form=form)














