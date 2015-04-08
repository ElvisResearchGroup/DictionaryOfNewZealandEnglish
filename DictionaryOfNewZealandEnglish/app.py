# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template

from DictionaryOfNewZealandEnglish.settings import ProdConfig
from DictionaryOfNewZealandEnglish.assets import assets
from DictionaryOfNewZealandEnglish.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    debug_toolbar,
)
from DictionaryOfNewZealandEnglish import public, user, headword
from DictionaryOfNewZealandEnglish.headword import attribute, citation, flag, register


def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    db.init_app(app)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
#    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
#        db.create_all()
    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(headword.views.blueprint)
    app.register_blueprint(attribute.views.blueprint)
    app.register_blueprint(citation.views.blueprint)
    app.register_blueprint(flag.views.blueprint)
    app.register_blueprint(register.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
