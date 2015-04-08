# -*- coding: utf-8 -*-
#from flask import Blueprint, render_template
from flask import (Blueprint, request, render_template, flash, 
                   url_for, redirect, session, g)
from flask.ext.login import login_required, current_user, login_user, logout_user
from flask_wtf import Form
from DictionaryOfNewZealandEnglish.user.forms import RegisterForm
from DictionaryOfNewZealandEnglish.utils import flash_errors
from DictionaryOfNewZealandEnglish.user.models import User
from datetime import datetime


blueprint = Blueprint("user", __name__, url_prefix='/users',
                        static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    return render_template("users/show.html")


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                               email=form.email.data,
                               institution=form.institution.data,
                               country=form.country.data,
                               interest=form.interest.data,
                               updated_at=datetime.utcnow(),
                               password=form.password.data,
                               active=True    )
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))

    else:
        flash_errors(form)
        return render_template('users/new.html', form=form)


