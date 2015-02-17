# DictionaryOfNewZealandEnglish


## Project set-up

### virtualenv
ref: http://docs.python-guide.org/en/latest/dev/virtualenvs/

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

Add autoenv which automagically activates the environment on cd-ing into the folder
    $ git clone git://github.com/kennethreitz/autoenv.git ~/.autoenv
    $ echo 'source ~/.autoenv/activate.sh' >> ~/.zshrc

