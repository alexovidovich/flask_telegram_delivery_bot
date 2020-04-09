from models import *
from datetime import datetime, timedelta
from business.basket_repr import *
from business.getting_info import *
from business.object_to_send import *
import os.path
from app import main_url
from business.basket import *
import pytz
from business.handler import *



def reduce_or_increase(data):
    data = data.split(',')
    if data[0].isdigit():
        if len(data)>1:
            return True , data[1],data[0]
        else:
            return True , None,data[0]
    else:
        return False , None,data[0]

class Interceptor:
    @staticmethod
    def interceptor_for_basket(data):
        if 'call_back' in data:
            

            result, order ,menu_pos_id = reduce_or_increase(data['call_back'])
            if result:
                plus_or_minus = None
                remove = None
                if order == 'delete_this_position':
                    remove = True
                elif order == 'reduce':
                    plus_or_minus = False
                elif order == 'increase':
                    plus_or_minus = True
                elif order == 'activate':

                    representation.repr(data) 
                #узнать адресс, номер а затем функция создания модели заказа и удаления корзины
                if not order == 'activate':
                    client = Client.query.filter(Client.chat_id == data['chat_id']).first()
                    print(client)
                    menu_position = Menu.query.filter(Menu.id == menu_pos_id).first()
                    print(menu_position)
                    create_basket_obj.create_if_not_exists()
                    print(data_to_read.reading_json('baskets_json'))
                    yes_or_not = check.check_if_exists(client)

                    basket = Basket_py(client,menu_position,yes_or_not,message_id=data['message_id'],plus_or_minus=plus_or_minus,remove=remove)
                    return True
            if data['call_back']== 'getaddress':
                if check.check_if_exists_something_inside(data['chat_id']):

                    obj = Object.return_obj(data['chat_id'],'Введите корректный адресс доставки (Город,улица,дом,номер квартиры)')
                    Send(main_url,'sendMessage',obj)
                    
                    time = str(datetime.now(pytz.timezone('Europe/Minsk'))+timedelta(minutes=5))

                    if not os.path.exists('./static/remember_message.json'):
                        ch_ms_id = [{data['chat_id']:[time,{'message_address':'not','message_phone':'not'}]}]
                        data_to_read.writting_json(ch_ms_id,'remember_message')
                    else:
                        check.check_remember_message(data['chat_id'])
                        add = data_to_read.reading_json('remember_message') 
                        if add == []:
                            ch_ms_id = [{data['chat_id']:[time,{'message_address':'not','message_phone':'not'}]}]
                            data_to_read.writting_json(ch_ms_id,'remember_message')                        
                        flag =True
                        print(add,'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
                        for i in add:
                            if data['chat_id'] in i:
                                flag = False
                                break
                        if flag == True:
                            ch_ms_id = {data['chat_id']:[time,{'message_address':'not','message_phone':'not'}]}
                            add.append(ch_ms_id)
                            data_to_read.writting_json(add,'remember_message')
                    return True
                else:
                    obj = Object.return_obj(data['chat_id'],'Ваша корзина пуста, выберете что-то вкусненькое, для того, чтобы сделать заказ!!!')
                    Send(main_url,'sendMessage',obj)

            if data['call_back']== 'make_order':
                Handler.make_ord(data)
                
            if data['call_back']== 'clean':
            
                print('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
                representation.delete(data)
                return True
        else:
            return False    

    
    @staticmethod
    def interceptor(data,pattern,worker):
        if 'text' in data :
            if data['text']:
                print('he')  
                print(data['text'])
                if not 'Ваш заказ пуст' in data['text']:
                    
                    
                    print('oooo')
                    for each in pattern:
                        print(each,data['text'])
                        if each.lower() in data['text'].lower() :

                            print(pattern,'WORKER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                            worker(data)

                            return True
                    return False
                else:
                    Basket_py.dell_2(data['chat_id'])



