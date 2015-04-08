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
from DictionaryOfNewZealandEnglish.headword.forms import *
from DictionaryOfNewZealandEnglish.public.forms import LoginForm
from DictionaryOfNewZealandEnglish.headword.models import *
from DictionaryOfNewZealandEnglish.headword.citation.models import *
from DictionaryOfNewZealandEnglish.database import engine
import datetime as dt
from operator import itemgetter

blueprint = Blueprint("register", __name__, url_prefix='/headwords/registers',
                        static_folder="../../static")


@blueprint.route("/delete", methods=["GET"])
@login_required
def delete():
    register = request.args.get('register')
    headword = request.args.get('headword')
    register = Register.query.filter_by(name=register).first()
    headword = Headword.query.filter_by(headword=headword).first()
    if register in headword.registers:
      headword.registers.remove(register)
      db.session.add(headword)
      db.session.commit()

    citations = headword.citations
    return render_template("headwords/show.html", headword=headword,
                                                  citations=citations)
