# -*- coding: utf-8 -*-
#from flask import Blueprint, render_template
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required

from DictionaryOfNewZealandEnglish.user.forms import DataForm
from DictionaryOfNewZealandEnglish.user.models import Citation
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





@blueprint.route("/search/", methods=["GET", "POST"])
@login_required
def search():
    # logged in users arrive here

    # Handle search
    #if request.method == 'POST':
    #    if form.validate_on_submit():
    form = DataForm(request.form, "search_data")


     #   else:
      #      flash_errors(form)
    return render_template("users/search.html", form=form)


@blueprint.route("/search/db", methods=["GET", "POST"])
def searchdb():
    flash('Searching data - this page should display responses, but doesn\'t yet.')
    form = DataForm(request.form, "display_data")
    return render_template("users/search.html", form=form)
