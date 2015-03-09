
import datetime
from DictionaryOfNewZealandEnglish.user.models import Citation
from DictionaryOfNewZealandEnglish.user.models import User
from DictionaryOfNewZealandEnglish.database import db_session
from DictionaryOfNewZealandEnglish.database import init_db

init_db()



date_obj = datetime.datetime.strptime('01/08/1452', '%d/%m/%Y').date() 
cit = Citation('Max', 'my diary', date_obj)

db_session.add(cit)  
db_session.commit() 

Citation.query.all()




u = User.create(username='Phil',
                        email='p@m.com',
                        password='1234567',
                        active=True)
#u = User('Matt', 'm@m.com')
db_session.add(u)          
db_session.commit()  

User.query.all()


from DictionaryOfNewZealandEnglish.user.models import Citation
Citation.query.all()


