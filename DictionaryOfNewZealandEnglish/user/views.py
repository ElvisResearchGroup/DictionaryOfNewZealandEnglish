# -*- coding: utf-8 -*-
# Users

from flask import (Blueprint, request, render_template, flash,
                   url_for, redirect, session)
from DictionaryOfNewZealandEnglish.extensions import bcrypt
from flask.ext.login import login_required, current_user, logout_user
from DictionaryOfNewZealandEnglish.user.forms import *
from DictionaryOfNewZealandEnglish.utils import flash_errors
from DictionaryOfNewZealandEnglish.user.models import User
from datetime import datetime as dt
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from DictionaryOfNewZealandEnglish.database import db


blueprint = Blueprint("user", __name__, url_prefix='/users',
                        static_folder="../static")


@blueprint.route("/", methods=['GET', 'POST'])
@login_required
def members():
    form = RegisterForm(request.form, obj=current_user, csrf_enabled=False)
    return render_template("users/show.html", user=current_user,
                                              form=form,
                                              action='edit')


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
                               updated_at=dt.utcnow(),
                               password=form.password.data,
                               active=True    )
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))

    else:
        flash_errors(form)
        return render_template('users/new.html', form=form)


@blueprint.route("/edit", methods=["POST"])
@login_required
def edit():
    user = User.query.filter_by(id=current_user.id).first()

    form = UserForm(request.form, obj=user, csrf_enabled=False)
    user_email = request.form['email']

    if request.method == "POST" and form.validate_on_submit():
      data = __set_data_for_user(user, form)
      if data:
        flash("Edit of %s is saved." % data.username, 'success')

    return render_template("users/show.html", user=user,
                                              form=form,
                                              action='edit')

@blueprint.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('public.home'))
    email = ""
    user = None
    searchForm = SearchForm(request.form)
    adminForm = None
    copy_request_form = request.form
    all_users = User.query.all()
    if request.method == "POST":
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
          # adjust admin status
          if 'is_admin' in request.form:
            is_admin = request.form['is_admin']
            checked = False
            if is_admin and is_admin=='y':
               checked = True
            User.update(user,
                        updated_at  = dt.utcnow(),
                        is_admin = checked)
            user = User.query.filter_by(email=email).first()
          elif user.id != current_user.id:
            # does not allow current admin user to "un-admin" themselves
            User.update(user,
                        updated_at  = dt.utcnow(),
                        is_admin = False)
          else:
            flash("An administrator cannot withdraw their own administrator " +
                  "privilages", 'warning')

          # delete user
          if 'delete_user' in request.form:
            # does not allow current user to delete themselves
            if user.id != current_user.id:
              User.delete(user)
              flash(user.username + " has been deleted", 'warning')
              user = None
              copy_request_form = request.form.copy()
              copy_request_form['email'] = ""
            else:
              flash("An administrator cannot delete thier own account", 'warning')


          searchForm = SearchForm(copy_request_form, obj=user)
          adminForm = AdminForm(request.form)

    return render_template("users/admin.html", user=user,
                                              form=searchForm,
                                              adminForm=adminForm,
                                              all_users=all_users)


##########################################################################
## private methods

def __set_data_for_user(user, form):
    try:
        if form.username.data:
          User.update(user,
                      username    = form.username.data,
                      updated_at  = dt.utcnow()   )
        if form.email.data:
          User.update(user,
                      email       = form.email.data,
                      updated_at  = dt.utcnow()   )
        if form.institution.data:
          User.update(user,
                      institution = form.institution.data,
                      updated_at  = dt.utcnow()   )
        if form.country.data:
          User.update(user,
                      country     = form.country.data,
                      updated_at  = dt.utcnow()   )
        if form.interest.data:
          User.update(user,
                      interest    = form.interest.data,
                      updated_at  = dt.utcnow()   )
        if form.password.data:
          User.update(user,
                      password    = bcrypt.generate_password_hash(form.password.data),
                      updated_at  = dt.utcnow()   )

    except (IntegrityError, InvalidRequestError):
        db.session.rollback()
        flash("The email %s is already taken." % form.email.data, 'warning')
        return None

    return User.query.filter_by(email=form.email.data).first()
