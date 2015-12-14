# DictionaryOfNewZealandEnglish

A web interface to the "Dictionary of New Zealand English", managed and run by the New Zealand Dictionary Center.

Written using Flask, a Python framework similar to Django but considerably lighter. Flask uses WTForms and SQLAlchemy.

These are development notes and stuff not committed to memory.


## Quick-start Project set-up

In the production environment, make sure the ``DNZE_ENV`` environment variable is set to ``"prod"``.

Set the secret key to something hard to guess.

Delete the python file "nzdc_data_massage.py" from the production code.
"manage.py" may need referances to this file deleted.

Once the server is set-up, initialise the database with;

    $ python manage.py data_import all:db

This will set up two users that will need thier passwords updated.

- username: admin, password: qwerty
- username: matt,  password: qwerty

New users register on the site. An administrator may then update user
privalages to become an admin and admins may delete existing users.

Enjoy!

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

NB: The shell script is not great, it calls activate on every sub folder.


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

Now start up the database and restart the server.


### Database Set-up

#### To manually reset Test Database
If you have already installed your database.

    $ python manage.py db init      
    $ python manage.py db migrate
    $ python manage.py db upgrade

    Stop the server using Ctl-c
    $ python manage.py server

The 'init' creates the database 'dev.db' and the migration folder & contents.
The 'migrate' will generate a new migration script.
And 'upgrade' applies the migration.

Seed data has been added to manage.py
This populates all the secondary tables and provides sufficient data for testing for the main two tables (Headword and Citations).

    $ python manage.py seed


#### Set-up a small production database (102 entries)

    python manage.py data_import Q:db


#### Adding db Notes to existing data text files (one-off operation)

    python manage.py data_import Q
    python manage.py data_import all

#### Set-up production Database -

Once only, further runs will reset the database to Nov 2015.
Takes around an hour to load all data.

    python manage.py data_import all:db


### Fixing missing spaces.

We can fix missing spaces in the raw import data by running a spell checker
over the fields which have missing spaces.  When a spelling error is detected,
if the suggested replacement is a space, then we do that, otherwise we ignore
the detected spelling error.  (It might not be a real spelling error)

The tricky bit is getting a new zealand language dictionary for pyenchant to use
in the hopes it will pickup words like Tekapuna etc.  Download the [openoffice
dictionary](http://extensions.services.openoffice.org/en/project/dict-en-nz-2008-12-03). Rename the oxt extension to .zip and extract the files to /usr/share/hunspell
Then pyenchant should be able to use it.  Test the dictionary.
```python
import enchant
enchant.list_languages() # language should be in the list_languages
b = enchant.Broker()
b.describe() # Lists the spelling engines
b.request_dict("en_NZ").provider #shows the provider for en_NZ -> should be hunspell or myspell
d = enchant.Dict("en_NZ")
d.tag # should return en_NZ
d.check("Nescafé") #should return true
d.check("Kiwiana") #should return true

```

Use http://stackoverflow.com/questions/23314834/tokenizing-unsplit-words-from-ocr-using-nltk



### fabric
ref: http://www.jeffknupp.com/blog/2012/02/09/starting-a-django-project-the-right-way/
A deployment tool. "pip install fabric", then add a fabfile.py with these contents.

NB: I may remove this.

    from fabric.api import local

    def prepare_deployment(branch_name):
        local('python manage.py test myapp')
        local('git add -p && git commit')
        local('git checkout master && git merge ' + branch_name)

    from fabric.api import lcd

    def deploy():
        with lcd('/path/to/my/prod/area/'):
            local('git pull /my/path/to/dev/area/')
            local('python manage.py migrate myapp')
            local('python manage.py test myapp')
            local('/my/command/to/restart/webserver')

### Shell

    $ python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``User`` model.


### Run all Tests

Note, no automated tests at this time. See spreadsheet of manual tests.

    $ python manage.py test

### App Time

Use UTC time throughout to avoid international time zone issues.
eg: datetime.datetime.utcnow instead of datetime.datetime.now


## Database overview
As at March 2015


###### User

| field                | type     | stuff            |
|----------------------|----------|------------------|
| id                   | int      | pk               |
| username             | char(80) | unique, not null |
| email                | char(80) | unique, not null |
| first_name           | char(30) |                  |
| last_name            | char(30) |                  |
| institution          | char(50) |                  |
| country              | char(50) |                  |
| interest             | text     |                  |
| password             | char(128)| hashed password  |
| active               | boolean  | default=false    |
| is_admin             | boolean  | default=false    |
| created_at           | date     | default=now      |
| updated_at           | date     | not null         |


###### Headword

| field                | type     | stuff         |
|----------------------|----------|---------------|
| id                   | int      | pk            |
| name                 | char(50) | not null      |
| definition           | text     | not null      |
| see                  | text     |               |
| pronunciation        | text     |               |
| notes                | text     |               |
| archived             | boolean  | default=false |
| data_set_id          | int      | fk            |
| homonym_number_id    | int      | fk            |
| word_class_id        | int      | fk            |
| sense_number_id      | int      | fk            |
| origin_id            | int      | fk            |
| domain_id            | int      | fk            |
| region_id            | int      | fk            |
| created_at           | date     | default=now   |
| updated_at           | date     | not null      |
| updated_by           | char(80) | not null      |


###### Citation

| field                | type     | stuff         |
|----------------------|----------|---------------|
| id                   | int      | pk            |
| date                 | date     | not null      |
| circa                | boolean  | default=false |
| author               | char(50) | not null      |
| source_id            | int      | fk            |
| vol_page             | char(50) |               |
| edition              | char(50) |               |
| quote                | text     |               |
| notes                | text     |               |
| created_at           | date     | default=now   |
| updated_at           | date     | not null      |
| updated_by           | char(80) | not null      |


##### Secondary tables
This format is used by 10 tables;
homonym_numbers, word_classes, sense_numbers, domains, regions,
origins, sources, data_sets, registers, flags.

| field                | type     | stuff         |
|----------------------|----------|---------------|
| id                   | int      | pk            |
| name                 | char(50) | not null      |
| notes                | text     |               |
| created_at           | date     | default=now   |


##### Many to Many join tables

###### headword_citations

| field                | type     | stuff    |
|----------------------|----------|----------|
| headword_id          | int      | fk       |
| citation_id          | int      | fk       |


###### headword_flags

| field                | type     | stuff    |
|----------------------|----------|----------|
| headword_id          | int      | fk       |
| flag_id              | int      | fk       |


###### headword_registers

| field                | type     | stuff    |
|----------------------|----------|----------|
| headword_id          | int      | fk       |
| register_id          | int      | fk       |
