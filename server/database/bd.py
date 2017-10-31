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

users = {'C0deMaver1ck': 'CorrectHorseBatteryStaple', 'dron94': '1234', 'svyat': '1111'} #Just dict with user's logins and passwords

if __name__ == '__main__':

    client = User('anton', '0000')
    new_tokin = client.create_tokin()
    tokin_dict[new_tokin] = client
    print(tokin_dict.keys())
    print(client.login, client.tokin)
