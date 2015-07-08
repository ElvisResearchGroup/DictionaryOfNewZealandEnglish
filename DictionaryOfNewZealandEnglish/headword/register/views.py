# -*- coding: utf-8 -*-

from flask import (Blueprint, request, render_template, url_for,
                    redirect, session)
from flask.ext.login import login_required, current_user
from DictionaryOfNewZealandEnglish.database import db
from DictionaryOfNewZealandEnglish.headword.forms import *
from DictionaryOfNewZealandEnglish.headword.models import *
from DictionaryOfNewZealandEnglish.headword.citation.models import *

blueprint = Blueprint("register", __name__, url_prefix='/headwords/registers',
                        static_folder="../../static")


@blueprint.route("/delete", methods=["GET"])
@login_required
def delete():
    if not current_user.is_admin:
        return redirect(url_for('public.home'))

    register = request.args.get('register')
    headword_id = request.args.get('headword_id')
    register = Register.query.filter_by(name=register).first()
    headword = Headword.query.get( headword_id )
    if register in headword.registers:
      headword.registers.remove(register)
      db.session.add(headword)
      db.session.commit()

    citations = headword.citations
    return render_template("headwords/show.html", headword=headword,
                                                  citations=citations)
