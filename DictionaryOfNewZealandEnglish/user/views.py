# -*- coding: utf-8 -*-
#from flask import Blueprint, render_template
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required

from DictionaryOfNewZealandEnglish.user.forms import DataForm
from DictionaryOfNewZealandEnglish.user.models import Citation
from DictionaryOfNewZealandEnglish.database import engine
import datetime

blueprint = Blueprint("user", __name__, url_prefix='/users',
                        static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    return render_template("users/members.html")



@blueprint.route("/insert/", methods=["GET", "POST"])
def insert():
    form = DataForm(request.form, used_as="insert_data")
    return render_template("users/insert.html", form=form)




@blueprint.route("/insert/db", methods=["GET", "POST"])
def insertdb():
    
    form = DataForm(request.form, used_as="insert_data")
    if form.validate():
      flash('Inserting data, in theory - still working on this. Validations are turned off.')
    else:
      flash('Inserting data, in theory - still working on this. Validate == FALSE ')

    date_obj = datetime.datetime.strptime(form.date.data, '%d/%m/%Y').date()
    citation = Citation.create(author = form.author.data,
                               source = form.source.data,
                               date   = date_obj )

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














