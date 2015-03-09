
# added but not implemented. Not convinced its needed yet,

"""
from fabric.api import local

myapp = "DictionaryOfNewZealandEnglish"

def prepare_deployment(branch_name):
    local('python manage.py test ' + myapp)
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)

from fabric.api import lcd

def deploy():
    with lcd('/path/to/my/prod/area/'):
        local('git pull /my/path/to/dev/area/')
        local('python manage.py migrate ' + myapp)
        local('python manage.py test ' + myapp)
        local('/my/command/to/restart/webserver')

"""

