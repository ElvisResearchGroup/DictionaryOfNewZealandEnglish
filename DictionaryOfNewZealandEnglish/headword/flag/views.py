# -*- coding: utf-8 -*-

from flask import (Blueprint, request, render_template, url_for,
                    redirect, session)
from flask.ext.login import login_required, current_user
from DictionaryOfNewZealandEnglish.database import db
from DictionaryOfNewZealandEnglish.headword.forms import *
from DictionaryOfNewZealandEnglish.headword.models import *
from DictionaryOfNewZealandEnglish.headword.citation.models import *

blueprint = Blueprint("flag", __name__, url_prefix='/headwords/flags',
                        static_folder="../../static")


@blueprint.route("/delete", methods=["GET"])
@login_required
def delete():
    if not current_user.is_admin:
        return redirect(url_for('public.home'))

    flag     = request.args.get('flag')
    headword_id = request.args.get('headword_id')
    flag     = Flag.query.filter_by(name=flag).first()
    headword = Headword.query.get( headword_id )
    if flag in headword.flags:
      headword.flags.remove(flag)
      db.session.add(headword)
      db.session.commit()

    citations = headword.citations
    return render_template("headwords/show.html", headword=headword,
                                                  citations=citations)
