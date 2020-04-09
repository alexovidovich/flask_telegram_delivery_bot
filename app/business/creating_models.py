import time
from models import Client
from models import db
from business.basket import *

def check_user(chat_id):
    begin = time.time()
    User = Client.query.filter(Client.chat_id == chat_id).first()
    # db.session.query(Client).delete()
    # db.session.commit()
    print(time.time()-begin)
    print(User)
    if User:
        return False
    return True
class Creating_model_client:

    @classmethod
    def creating_client(cls,data):
        dict_data = data
        if check_user(dict_data['chat_id']):
            new_client = Client(name = dict_data['name'],chat_id = dict_data['chat_id'],teleg_id =dict_data['teleg_id'] )
            db.session.add(new_client)
            db.session.commit()
class Creating_order:
    @staticmethod
    def create(chat_id,addres):
        Basket_py.create_order(chat_id,addres)
        Basket_py.dell(chat_id)


    
    

        



        
       