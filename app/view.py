from app import *
from flask import request
import json
from business.getting_info import data_to_read
from datetime import datetime,timedelta
from business.basket_repr import representation
import pytz
import time
from models import *
from business.creating_models import Creating_model_client
from business.interceptor_requests import Interceptor
from business.handler import *
from business.orders_repr import *
@app.route('/',methods= ['POST','GET'])
def index():
    

    # id-c teleg_id-c number-c chat_id-c name-c address-c orders-[<>,]


    #-----------
    begin = time.time()
    json_data=data_to_read.getting_info()#1
    print('1',time.time() - begin,'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=')
    data_to_read.writting_json(data = json_data,name='json_api_update')#2
    print('2',time.time() - begin,'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=')
    data = data_to_read.mapping_info_user()#3
    if data != None:
        print('3',time.time() - begin,'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=')
        Creating_model_client.creating_client(data)#4
        
            
        
        print('4',time.time() - begin,'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=')
        if Interceptor.interceptor(data=data,pattern=['/start','start','begin','начать','привет'],worker=Handler.if_start) == True:
            print('start')#5
            print('5',time.time() - begin,'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=')
        elif Interceptor.interceptor(data=data,pattern=['Меню','позиции','еда','еду','food'],worker=Handler.if_menu)==True:
            print('меню')#6
        
            print('6',time.time() - begin,'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=')
        elif Interceptor.interceptor_for_basket(data = data)==True:
            print('callback')#7
            print('7',time.time() - begin,'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=')
        elif Interceptor.interceptor(data=data,pattern=['Корзина','basket'],worker=representation.repr)==True:
            print('Корзина')#8
            print('8',time.time() - begin,'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=')
        elif Interceptor.interceptor(data=data,pattern=['Заказы','orders'],worker=Repr.represent)==True:
            print('Заказы')#9
            print('9',time.time() - begin,'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=')
        else:

        
        
            Interceptor.interceptor(data=data,pattern=[''],worker=Handler.if_any)
            print(data['text'])
    return '<h1>e</h1>'



@app.route('/orders',methods= ['POST','GET'])
def orders():
    return '<h1>orders</h1>'
