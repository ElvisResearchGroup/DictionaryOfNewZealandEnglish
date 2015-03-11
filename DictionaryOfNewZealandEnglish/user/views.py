# -*- coding: utf-8 -*-
#from flask import Blueprint, render_template
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required
from flask_wtf import Form
import DictionaryOfNewZealandEnglish.utils as utils
import logging
import sys

from DictionaryOfNewZealandEnglish.user.forms import HeadwordForm, RegisterForm, TableEditForm
from DictionaryOfNewZealandEnglish.public.forms import LoginForm
from DictionaryOfNewZealandEnglish.user.models import Headword
from DictionaryOfNewZealandEnglish.user.models import Citation, Word_class, Data_set
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
    form = HeadwordForm(request.form, "search_data")
    return render_template("users/search.html", form=form)


@blueprint.route("/search/db", methods=["POST"])
@login_required
def searchdb():
    form = HeadwordForm(request.form, "display_data")
    # Handle search
    if form.validate_on_submit():
        #author = form.author.data
        #source = form.source.data
        try:
            date = dt.datetime.strptime(form.updated_at.data, '%d/%m/%Y').date()
        except ValueError:
            date = ""

        #citations = Citation.query.filter_by(author="Wallace", source="maximum").all()
        #citations = engine.execute('select * from Citations where author = :1', [author]).first()

        flash('Search form is validated ')# + citations[0].source)

    else:
        flash_errors(form)

    #flash('Searching data - this page should display responses, but doesn\'t yet.')
    return render_template("users/search.html", form=form)


@blueprint.route("/table_list/", methods=["GET"])
@login_required
def table_list():
    table = request.args.get('table')
    data = data_for_table_rowname(table, 'all')
    return render_template("users/table_list.html", table=table, data=data)




@blueprint.route("/table_update/", methods=["GET", "POST"])
@login_required
def table_update():
    table = request.args.get('table')
    name = request.args.get('name')
    form = TableEditForm(request.form, "edit_table")
#    archived = True if 'archived' in form else False

    if request.method == "GET":
      data = data_for_table_rowname(table, name)
    if request.method == "POST":
      data = data_update_table_rowname(table, name, form)
      name = data.name

    return render_template("users/table_update.html", table=table, name = name, data=data, form=form)


#@blueprint.route("/table_update/", methods=["POST"])
#@login_required
#def table_update2():
#    table = request.args.get('table')
#    name  = request.args.get('name')
#    form  = TableEditForm(request.form, "edit_table")
#    data = data_update_table_rowname(table, name, form)

#    return render_template("users/table_update.html", table=table, name = data.name, data=data, form=form)


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

module_name = "DictionaryOfNewZealandEnglish.user.models"

# TODO find way to make this a private method... @private
def data_for_table_rowname(table, name):

    _class = str_to_class(module_name, table)

    if name == "all":
        return _class.query.all()
    else: 
        return _class.query.filter_by(name=name).first()



# TODO find way to make this a private method... @private
def data_update_table_rowname(table, name, form):

    _class = str_to_class(module_name, table)

    entry = _class.query.filter_by(name=name).first()
    #print '####', form.archived.data, form.archived.data=='y'
    #archived = True if form.archived.data else False
    
    _class.update(entry,
                  name=form.name.data,
                  notes=form.notes.data,
                  archived=form.archived.data
                 )
    return data_for_table_rowname(table, name)


# TODO move to utils.py
def str_to_class(module_name, class_name):
    class_name = class_name.replace(' ', '_')
    class_ = None
    try:
        module_ = utils.import_module(module_name)
        try:
            class_ = getattr(module_, class_name)
        except AttributeError:
            print 'Class does not exist'
            logging.error('Class does not exist')
    except ImportError:
        print 'Module does not exist', module_name
        logging.error('Module does not exist')
    return class_

