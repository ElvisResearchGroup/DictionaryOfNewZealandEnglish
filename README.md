# DictionaryOfNewZealandEnglish

A web interface to the "Dictionary of New Zealand English", managed and run by the New Zealand Dictionary Center.


Development notes and stuff I do not wish to commit to memory.


## Project set-up


### virtualenv
ref: http://docs.python-guide.org/en/latest/dev/virtualenvs/
Setup

    $ pip install virtualenv
    $ cd project_folder
    $ virtualenv venv

Activate

    $source venv/bin/activate

Future packages installed with pip are installed into the venv folder. eg:

    $ pip install requests

To deactivate (and use the systems default Python interpreter

    $ deactivate

To delete the venv, just remove the folder (rm -rf venv)

To freeze the dependency list

    $ pip freeze > requirements.txt

To recreate the environment later

    $ pip install -r requirements.txt

Add the venv folder to .git ignore 

    $ echo venv >> .gitignore

[optional] Add autoenv which automagically activates the environment on cd-ing into the folder

    $ git clone git://github.com/kennethreitz/autoenv.git ~/.autoenv
    $ echo 'source ~/.autoenv/activate.sh' >> ~/.zshrc
    $ cd to-directory-holding-the-venv-directory
    $ touch .env
    $ echo "echo '### automagically start venv ###'" > .env
    $ echo "source venv/bin/activate" >> .env

Test by cd-ing out of file and back in.
TODO: The shell script is not great, it calls activate on every sub folder... Will find solution later.


### cookiecutter
ref: https://github.com/sloria/cookiecutter-flask
Setup

    $ pip install cookiecutter
    $ cookiecutter https://github.com/sloria/cookiecutter-flask.git

Note: Project file was already set up. When cookiecutter was used, had to drag directories into the main folder. Used app name of DictionaryOfNewZealandEnglish in case of hidden dependencies.

Set your app's secret key as an environment variable. For example, example add the following to ``.bashrc`` or ``.bash_profile`` or .zshrc.

    export DNZE_SECRET='something-really-secret'

Then run the following commands to bootstrap your environment.
Note that a database has not yet been added.

    $ cd to-main-project-directory
    $ pip install -r requirements/dev.txt
    $ python manage.py server

Visit localhost:5000 on your server and you should see a lovely Welcome page.

If you have already installed your database.

    $ python manage.py db init
    $ python manage.py db migrate
    $ python manage.py db upgrade
    $ python manage.py server

Note: these worked after half an hour without having to do anything more. It seems the database is installed, it must be magic...



## README storage space

These are copied from the cookiecutter readme file. Placed here until I can better put them into a setup context.

### Deployment

In your production environment, make sure the ``DNZE_ENV`` environment variable is set to ``"prod"``.


### Shell

To open the interactive shell, run ::

    $ python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``User`` model.


### Running Tests

To run all tests, run ::

    $ python manage.py test


### Migrations

Whenever a database migration needs to be made. Run the following commmands:

    $ python manage.py db migrate

This will generate a new migration script. Then run:

    $ python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``. 


