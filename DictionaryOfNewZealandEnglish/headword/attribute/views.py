# -*- coding: utf-8 -*-

from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required, current_user
import DictionaryOfNewZealandEnglish.utils as utils
import logging
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from DictionaryOfNewZealandEnglish.database import db
from DictionaryOfNewZealandEnglish.headword.attribute.forms import *
from DictionaryOfNewZealandEnglish.headword.attribute.models import *
from DictionaryOfNewZealandEnglish.headword.citation.models import *
import datetime as dt

blueprint = Blueprint("attribute", __name__, url_prefix='/headwords/attributes',
                        static_folder="../static")


@blueprint.route("/index", methods=["GET"])
@login_required
def index():
    if not current_user.is_admin:
        return redirect(url_for('public.home'))
    table = request.args.get('table')
    headword = Headword.query.get( request.args.get('headword_id') )
    citation = None
    if request.args.get('citation_id'):
      citation = Citation.query.get( request.args.get('citation_id') )
    data = __get_data_for_table_rowname(table, 'all')
    form = TableEditForm(request.form, "edit_table")
    return render_template("headwords/attributes/index.html", table=table,
                                                              headword=headword, 
                                                              citation=citation,
                                                              data=data, 
                                                              Flag=Flag,
                                                              Register=Register,
                                                              Source=Source,
                                                              Headword=Headword,
                                                              form=form)


@blueprint.route("/create", methods=["POST"])
@login_required
def create():
    if not current_user.is_admin:
        return redirect(url_for('public.home'))
    table = request.args.get('table')
    form = TableEditForm(request.form, "edit_table")
    citation_id = request.args.get('citation_id')
    citation = None
    if citation_id:
      citation = Citation.query.get( citation_id )
    headword = Headword.query.get( request.args.get('headword_id') )
    name = form.name.data
    __create_row_in_table_for_name(table, form)
    data = __get_data_for_table_rowname(table, 'all')
    form.name.data = ""

    return render_template("headwords/attributes/index.html", table=table, 
                                                              headword=headword,
                                                              citation_id=citation_id,
                                                              citation=citation,
                                                              data=data,
                                                              Flag=Flag,
                                                              Register=Register,
                                                              Source=Source,
                                                              form=form)


@blueprint.route("/delete", methods=["GET"])
@login_required
def destroy():
    if not current_user.is_admin:
        return redirect(url_for('public.home'))

    table = request.args.get('table')
    name = request.args.get('name')
    headwords = None
    data = __get_data_for_table_rowname(table, name)

    # data == None if user has refreshed view after delete has been completed
    if data != None:
      # do not delete a data row if it will leave hanging db entries
      if table == 'Register' or table == 'Flag':
        if table == 'Register':
          register = Register.query.filter_by(name=name).first()
          headwords = register.headwords
        else:
          flag = Flag.query.filter_by(name=name).first()
          headwords = flag.headwords
        count = 0
        for i in headwords:
          count += 1

      else:
        _table = str_to_class(module_name, table).query.filter_by(name=name).first()
        if table == "Source":
          source_attribute_id = getattr(Citation,'source_id')
          count = Citation.query.filter(source_attribute_id == _table.id).count()
        else:
          headword_attribute_id = getattr(Headword,'%s_id' % table.lower().replace(' ', '_'))
          count = Headword.query.filter(headword_attribute_id == _table.id).count()
      
      if count == 0:
          data = __delete_row_in_table(table, name)
      else:
          flash("Cannot delete %s as it is in use by %s headwords" % (name, count), 'warning') 

    data = __get_data_for_table_rowname(table, 'all')
    form = TableEditForm(request.form, "edit_table")
    headword = Headword.query.get( request.args.get('headword_id') )
    citation = None
    if request.args.get('citation_id'):
      citation = Citation.query.get( request.args.get('citation_id') )
    return render_template("headwords/attributes/index.html", table=table, 
                                                              headword=headword,
                                                              citation=citation,
                                                              data=data, 
                                                              Flag=Flag,
                                                              Register=Register,
                                                              Source=Source,
                                                              form=form)


@blueprint.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if not current_user.is_admin:
        return redirect(url_for('public.home'))

    table = request.args.get('table')
    name = request.args.get('name')
    headword_id = request.args.get('headword_id')
    citation_id = request.args.get('citation_id')
    form = TableEditForm(request.form, "edit_table")

    if request.method == "GET":
      data = __get_data_for_table_rowname(table, name)
      headword = Headword.query.get( headword_id )
      return render_template("headwords/attributes/edit.html", 
                              table = table, 
                              name  = name, 
                              headword=headword,
                              citation_id=citation_id,
                              data  = data, 
                              form  = form)

    if request.method == "POST":
      data = set_data_for_table_rowname(table, name, form)
      flash("Edit of %s is saved." % data.name, 'success')
      if isinstance(data, basestring):
        flash(data)
        data = __get_data_for_table_rowname(table, name)
      else:
        name = data.name

      return redirect("headwords/attributes/index?table={0}&headword_id={1}&citation_id={2}".format(table, headword_id, citation_id))


#############################################################################
# private methods #

module_name = "DictionaryOfNewZealandEnglish.headword.attribute.models"

def __create_row_in_table_for_name(table, form):

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
    return __get_data_for_table_rowname(table, name)

def __delete_row_in_table(table, name):

    _class = str_to_class(module_name, table)
    db_row = _class.query.filter_by(name=name).first()

    try:
        _class.delete(db_row)

    except (IntegrityError, InvalidRequestError):
        db.session.rollback()
        return "Database integrety constraint: %s has a problem" % name

    flash("%s deleted from database: " % name, 'success')
    return __get_data_for_table_rowname(table, 'all')


def __get_data_for_table_rowname(table, name):

    _class = str_to_class(module_name, table)

    if name == "all":
        l =  _class.query.all()
        l = sorted(l, key=lambda origin: origin.name.lower() )
        l = sorted(l, key=lambda origin: origin.archived )
        return l
    else: 
        return _class.query.filter_by(name=name).first()


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

    return __get_data_for_table_rowname(table, new_name)


def str_to_class(module_name,class_name):
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

