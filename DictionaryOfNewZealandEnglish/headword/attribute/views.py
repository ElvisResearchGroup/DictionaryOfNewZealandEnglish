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
from DictionaryOfNewZealandEnglish.headword.attribute.forms import *
from DictionaryOfNewZealandEnglish.headword.attribute.models import *
from DictionaryOfNewZealandEnglish.public.forms import LoginForm
from DictionaryOfNewZealandEnglish.database import engine
import datetime as dt
from operator import itemgetter

blueprint = Blueprint("attribute", __name__, url_prefix='/headwords/attributes',
                        static_folder="../static")



@blueprint.route("/index", methods=["GET"])
@login_required
def index():
    table = request.args.get('table')
    data = get_data_for_table_rowname(table, 'all')
    form = TableEditForm(request.form, "edit_table") # for new entries
    return render_template("headwords/attributes/index.html", table=table, data=data, form=form)


@blueprint.route("/create", methods=["POST"])
@login_required
def create():
    table = request.args.get('table')
    form = TableEditForm(request.form, "edit_table")
    name = form.name.data
    create_row_in_table_for_name(table, form)
    data = get_data_for_table_rowname(table, 'all')
    form.name.data = ""

    return render_template("headwords/attributes/index.html", table=table, data=data, form=form)


@blueprint.route("/delete", methods=["GET"])
@login_required
def destroy():
    table = request.args.get('table')
    name = request.args.get('name')
    data = get_data_for_table_rowname(table, name)

    # case when refreshing view after delete has taken effect
    if data == None:
        data = get_data_for_table_rowname(table, 'all')
        form = TableEditForm(request.form, "edit_table") # for new entries
        return render_template("headwords/attributes/index.html", table=table, data=data, form = form)

    # TODO finish this recipe once Headwords can cope
    # do not deleting a data row if it will leave hanging db entries
    data = None # TODO get all headwords using this table & name
    if data == None:
        flash("TODO not yet checking database for existing use before deleting")
        # TODO if set is empty, display 'are you sure?' message
        data = delete_row_in_table(table, name)
        form = TableEditForm(request.form, "edit_table") # for new entries
        return render_template("headwords/attributes/index.html", table=table, data=data, form = form)
    else:
        flash("Cannot delete %s as it is in use in these records" % name) 
        # TODO render a page with list of (max 30?) headwords that will be affected


@blueprint.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    table = request.args.get('table')
    name = request.args.get('name')
    form = TableEditForm(request.form, "edit_table")
    if request.method == "GET":
      data = get_data_for_table_rowname(table, name)
      return render_template("headwords/attributes/edit.html", 
                              table = table, 
                              name  = name, 
                              data  = data, 
                              form  = form)
    if request.method == "POST":
      data = set_data_for_table_rowname(table, name, form)
      flash("Edit of %s is saved." % data.name, 'success')
      if isinstance(data, basestring):
        flash(data)
        data = get_data_for_table_rowname(table, name)
      else:
        name = data.name

      return redirect("headwords/attributes/index?table=%s" % table)


#############################################################################
# private methods #

module_name = "DictionaryOfNewZealandEnglish.headword.attribute.models"

def create_row_in_table_for_name(table, form):

    name=form.name.data
    _class = str_to_class(module_name, table)

    try:
        _class.create(
                      name=form.name.data,
                      notes=form.notes.data, 
                      archived=form.archived.data, 
                      updated_by=current_user.username, 
                      updated_at=dt.datetime.utcnow()
                      )

    except (IntegrityError, InvalidRequestError):
        db.session.rollback()
        return "Database integrety constraint: %s already exists in the database" % name

    flash("%s inserted into database: " % name, 'success')
    return get_data_for_table_rowname(table, name)

def delete_row_in_table(table, name):

    _class = str_to_class(module_name, table)
    db_row = _class.query.filter_by(name=name).first()

    try:
        _class.delete(db_row)

    except (IntegrityError, InvalidRequestError):
        db.session.rollback()
        return "Database integrety constraint: %s has a problem" % name

    flash("%s deleted from database: " % name, 'success')
    return get_data_for_table_rowname(table, 'all')


# TODO find way to make this a private method... @private
def get_data_for_table_rowname(table, name):

    _class = str_to_class(module_name, table)

    if name == "all":
        return _class.query.order_by('archived').order_by('name').all()
    else: 
        return _class.query.filter_by(name=name).first()



# TODO find way to make this a private method... @private
def set_data_for_table_rowname(table, name, form):

    _class = str_to_class(module_name, table)
    db_row = _class.query.filter_by(name=name).first()
    new_name = form.name.data

    try:
        _class.update(db_row,
                  name=new_name,
                  notes=form.notes.data,
                  archived=form.archived.data,
                  updated_by=current_user.username, 
                  updated_at=dt.datetime.utcnow()
                  )
    except (IntegrityError, InvalidRequestError):
        db.session.rollback()
        return "Database integrety constraint - %s already exists in the database" % new_name

    return get_data_for_table_rowname(table, new_name)


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

