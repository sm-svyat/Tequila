# Super mega thoughtful data base
import hashlib
import time

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

#tokin_dict = dict()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    tokin = Column(String)

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.tokin = ''

    def create_tokin(self):
        self.tokin = hashlib.sha224((time.ctime()+self.login).encode('utf-8')).hexdigest()

    def __repr__(self):
        return "<User('%s','%s')>" % (self.login, self.tokin)

    def getmsg(self):
        return self.client_message

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    from_id = Column(Integer)
    to_id = Column(Integer)
    time = Column(String)
    message = Column(String)

    def __init__(self, from_id, to_id, time, message):
        self.from_id = from_id
        self.to_id = to_id
        self.time = time
        self.message = message


    def __repr__(self):
        return '{}'.format({
            "from": self.from_id,
            "to": self.to_id,
            "time": self.time,
            "message": self.message
            })


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    contact_id = Column(Integer)
    accepted = False

    def __init__(self, user_id, contact_id):
        self.user_id = user_id
        self.contact_id = contact_id



users = {'C0deMaver1ck': 'CorrectHorseBatteryStaple', 'dron94': '1234', 'svyat': '1111'} #Just dict with user's logins and passwords

if __name__ == '__main__':

    client = User('anton', '0000')
    new_tokin = client.create_tokin()
    tokin_dict[new_tokin] = client
    print(tokin_dict.keys())
    print(client.login, client.tokin)
