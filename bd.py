# Super mega thoughtful data base
import hashlib
import time

tokin_dict = dict()

class User:
    #def __init__(self, client, addr):
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.client = object()
        self.addr = object()
        self.username = str()
        self.client_message = str()
        self.tokin = ''

    def create_tokin(self):
        self.tokin = hashlib.sha224((time.ctime()+self.login).encode('utf-8')).hexdigest()
        #return self.tokin

    def __str__(self):
        return self.username

    def __repr__(self):
        return '{}, {}'.format(self.login, self.tokin)

    def getmsg(self):
        return self.client_message

users = {'C0deMaver1ck': 'CorrectHorseBatteryStaple', 'dron94': '1234', 'svyat': '1111'} #Just dict with user's logins and passwords



#not used
response_list = [
    {
    "response": 200,
    "alert": "Необязательное сообщение/уведомление"
    }
    ]

if __name__ == '__main__':

    client = User('anton', '0000')
    new_tokin = client.create_tokin()
    tokin_dict[new_tokin] = client
    print(tokin_dict.keys())
    print(client.login, client.tokin)
