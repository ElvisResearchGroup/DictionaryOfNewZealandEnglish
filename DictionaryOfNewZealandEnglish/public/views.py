# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_user, login_required, logout_user
from datetime import datetime

from DictionaryOfNewZealandEnglish.extensions import login_manager
from DictionaryOfNewZealandEnglish.user.models import User
from DictionaryOfNewZealandEnglish.public.forms import LoginForm
#from DictionaryOfNewZealandEnglish.user.forms import RegisterForm
from DictionaryOfNewZealandEnglish.utils import flash_errors
from DictionaryOfNewZealandEnglish.database import db

blueprint = Blueprint('public', __name__, static_folder="../static")

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    login_form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if login_form.validate_on_submit():
            login_user(login_form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(login_form)
    #return render_template("public/home.html", form=form)
    return render_template("public/nzdchome.html", login_form=login_form)

@blueprint.route("/search/")
def search():
    login_form = LoginForm(request.form)
    return render_template("public/search.html", login_form=login_form)

#@blueprint.route("/about/")
#def about():
#    form = LoginForm(request.form)
#    return render_template("public/about.html", title="Fred", form=form)












