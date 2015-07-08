# -*- coding: utf-8 -*-

'''Public section, including homepage and signup.'''

from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect)
from flask.ext.login import login_user

from DictionaryOfNewZealandEnglish.extensions import login_manager
from DictionaryOfNewZealandEnglish.user.models import User
from DictionaryOfNewZealandEnglish.public.forms import LoginForm
from DictionaryOfNewZealandEnglish.utils import flash_errors

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
    return render_template("public/home.html", login_form=login_form)

@blueprint.route("/search/")
def search():
    login_form = LoginForm(request.form)
    return render_template("public/search.html", login_form=login_form)

@blueprint.route("/history")
def history():
    login_form = LoginForm(request.form)
    return render_template("public/history.html", login_form=login_form)

@blueprint.route("/publications")
def publications():
    login_form = LoginForm(request.form)
    return render_template("public/publications.html", login_form=login_form)




