from business.sending import *
from business.object_to_send import *
from business.getting_info import data_to_read
from models import *
from datetime import datetime, timedelta

from business.sending_key_board import InlineKeyboardMarkup,ReplyKeyboardMarkup
from app import main_url
import os.path
import pytz
import re 
utc=pytz.timezone('Europe/Minsk')


class create_basket_obj(object):
    @staticmethod
    def create_if_not_exists():
        if not os.path.exists('./static/baskets_json.json'):
            baskets_json = []
            data_to_read.writting_json(baskets_json,'baskets_json')


        # [{f'{self.client.chat_id}':[self.time,[{f'{self.menu_position.id}':1}]}]
class check(object):
    @staticmethod
    def check_if_exists(client):
        json_list = data_to_read.reading_json('baskets_json')
        for dict_ in json_list:
            if client.chat_id in dict_:
                return True
        return False
    @staticmethod
    def check_if_exists_something_inside(chat_id):
        json_list = data_to_read.reading_json('baskets_json')
        for dict_ in json_list:
            if chat_id in dict_:
                if len(dict_[chat_id][1])>0:
                    print('есть чет внутри')
                    return True
                    
        return False
    @staticmethod
    def check_remember_message(chat_id):
        json_list = data_to_read.reading_json('remember_message') 
            
        for each_el in json_list:
            _, values = zip(*each_el.items())
            values = list(values)[0][0]        
            values = values.split('+')
            date_time_obj = datetime.strptime(values[0], '%Y-%m-%d %H:%M:%S.%f')
            
            date_time_obj = pytz.timezone('Europe/Minsk').localize(date_time_obj)
            if date_time_obj < datetime.now(utc):
                json_list.remove(each_el)
                
            
        data_to_read.writting_json(json_list,'remember_message')
    @staticmethod
    def check_if_in_remember_mes(chat_id,data):
        print(data)
        json_list = data_to_read.reading_json('remember_message')
        for each in json_list:
            
            if chat_id in each:
                print(chat_id,each,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
                print(each[chat_id][1]["message_address"],'0000000000000000000000')
                if each[chat_id][1]["message_address"] == "not":
                    #можно добавить регулярное выражение для проверки адресса
                    each[chat_id][1]["message_address"] = data['text']
                    obj = Object.return_obj(chat_id,'Введите номер вашего телефона.+375xxxxx-xx-xx')
                    Send(main_url,'sendMessage',obj)
                    data_to_read.writting_json(json_list,'remember_message')
    
                else:
                    if each[chat_id][1]["message_phone"] == "not":
                        find = re.findall(r'[+]375\d\d\d\d\d-\d\d-\d\d',data['text']) or re.findall(r'[+]375\d\d\d\d\d\d\d\d\d',data['text'])
                        if find:
                            each[chat_id][1]["message_phone"] = data['text']
                            data_to_read.writting_json(json_list,'remember_message')
                            return True,each[chat_id][1]["message_address"],each[chat_id][1]["message_phone"]
                        else:
                            obj = Object.return_obj(chat_id,'Введите номер корректно, как в примере.')
                            Send(main_url,'sendMessage',obj)
                            data_to_read.writting_json(json_list,'remember_message')
                            return False,None,None
                    data_to_read.writting_json(json_list,'remember_message')
                    return False,None,None
                  
        return False,None,None
                            

                
        
        

                
class Basket_py(object):
    def __init__(self,client,menu_position,yes_or_not,message_id,plus_or_minus=None,remove=None):
        
        self.remove = remove
        self.message_id = message_id
        self.client = client
        self.already_have = False
        self.plus_or_minus = plus_or_minus
        self.menu_position = menu_position
        self.yes_or_not = yes_or_not
        self.time = datetime.now(utc)+timedelta(hours=1)
        self.death_time()
        print(self.remove,self.plus_or_minus)
        if self.yes_or_not == True:
            self.add()
        else:
            self.create()
        

    def create(self):
        self.json_list = data_to_read.reading_json('baskets_json')
        
        self.price_of_basket = self.menu_position.price
        self.personal_basket = {f'{self.client.chat_id}':[str(self.time), \
            [{f'{self.menu_position.id}':1}],self.price_of_basket,[{self.menu_position.id:self.message_id}]]}
        self.json_list.append(self.personal_basket)
        data_to_read.writting_json(self.json_list,'baskets_json')
        # кинуть обновление сообщения для функциии add 
        self.update_obj = Object.return_obj(self.client.chat_id,message_id=self.message_id, reply_markup=InlineKeyboardMarkup.update('1',str(self.menu_position.price),basket_price= str(self.price_of_basket),menu_id=str(self.menu_position.id)))
        #self.update_obj = Object.return_obj(self.client.chat_id,message_id=self.message_id,reply_markup=InlineKeyboardMarkup.lol('works'))
        Send(main_url,'editMessageReplyMarkup',self.update_obj)

    def add(self):
        self.json_list = data_to_read.reading_json('baskets_json')
        self.can_add = True
        for each_el in self.json_list:
            if self.client.chat_id in each_el:
                #-------------del_updating_messages------------
                if len(each_el[self.client.chat_id][3])>6:
                    each_el[self.client.chat_id][3].clear()
                #-------------del_updating_messages------------

                #-------------add_updating_messages------------
                for message in each_el[self.client.chat_id][3]:
                    _ , values = zip(*message.items())
                    if int(self.message_id) == int(list(values)[0]):    
                        self.can_add = False         

                if self.can_add==True:
                    new_dict_in_messages = {self.menu_position.id:self.message_id}
                    each_el[self.client.chat_id][3].append(new_dict_in_messages)
                #-------------add_updating_messages------------

                # self.basket_list = each_el[self.client.chat_id][1]
                for possition in each_el[self.client.chat_id][1]:

                    if str(self.menu_position.id) in possition:# если есть айдищник меню выбранного сейчас заказа в корзине позльзователя, 
                                                                #если нет, то добавить новую позицию в корзину со значением 1 шт
                        self.already_have = True
                        if self.plus_or_minus==True:
                            possition[str(self.menu_position.id)]+=1  # нужно будет тут редактировать кол-во + или - в зависимости от колбека
                            each_el[self.client.chat_id][2] += int(self.menu_position.price)     
                        elif self.plus_or_minus==False:
                            if possition[str(self.menu_position.id)]!=1:
                                possition[str(self.menu_position.id)]-=1 
                                each_el[self.client.chat_id][2] -= int(self.menu_position.price)# нужно будет тут редактировать кол-во + или - в зависимости от колбека




                        #--------------------------REMOVE-------------------------------------        
                        if self.remove ==True:
                            each_el[self.client.chat_id][2]-=possition[str(self.menu_position.id)] * float(self.menu_position.price)
                            possition[str(self.menu_position.id)]=0
                            if len(each_el[self.client.chat_id][1])== 0:
                                each_el[self.client.chat_id][2] = 0
                            for i in each_el[self.client.chat_id][3]:
                                self.pos_menu, self.mes_id = zip(*i.items())
                                self.pos_menu =list(self.pos_menu)[0]
                                self.mes_id = list(self.mes_id)[0]
                                self.pos_menu = Menu.query.filter(Menu.id==self.pos_menu).first()
                                self.value_of_posit = None
                                for i in each_el[self.client.chat_id][1]:
                                    if str(self.pos_menu.id) in i:
                                        self.value_of_posit = i[str(self.pos_menu.id)]
                                #-----------UPDATE------------
                                if self.value_of_posit != None:
                                    self.update_obj = Object.return_obj(self.client.chat_id,message_id=self.mes_id, \
                                        reply_markup=InlineKeyboardMarkup.update(str(self.value_of_posit ), \
                                            str(float(self.pos_menu.price)*float(self.value_of_posit)), \
                                                menu_id=str(self.pos_menu.id),basket_price= str(each_el[self.client.chat_id][2])))
                                    Send(main_url,'editMessageReplyMarkup',self.update_obj)
                                else:
                                    self.update_obj = Object.return_obj(self.client.chat_id,message_id=self.mes_id, \
                                        reply_markup=InlineKeyboardMarkup.update(str(0), \
                                            str(float(self.pos_menu.price)*float(0)), \
                                                menu_id=str(self.pos_menu.id),basket_price= str(each_el[self.client.chat_id][2])))
                                    Send(main_url,'editMessageReplyMarkup',self.update_obj)
                                #-----------UPDATE------------
                            each_el[self.client.chat_id][1].remove(possition)
                            #--------------------------REMOVE-----------------------------------------
                        else:
                                #(how_many,price_of_all,price_of_basket,menu_id
                            #-----------UPDATE------------
                            for i in each_el[self.client.chat_id][3]:
                                self.pos_menu, self.mes_id = zip(*i.items())
                                self.pos_menu =list(self.pos_menu)[0]
                                self.mes_id = list(self.mes_id)[0]
                                self.pos_menu = Menu.query.filter(Menu.id==int(self.pos_menu)).first()
                                for i in each_el[self.client.chat_id][1]:
                                    if str(self.pos_menu.id) in i:
                                        self.value_of_posit = i[str(self.pos_menu.id)]
                                        self.update_obj = Object.return_obj(self.client.chat_id,message_id=self.mes_id, \
                                            reply_markup=InlineKeyboardMarkup.update(str(self.value_of_posit ), \
                                                str(float(self.pos_menu.price)*float(self.value_of_posit)), \
                                                    menu_id = str(self.pos_menu.id),basket_price= str(each_el[self.client.chat_id][2])))
                                        Send(main_url,'editMessageReplyMarkup',self.update_obj)
                                    
                            #-----------UPDATE------------
                    
                        #---------adding object if not exists-------
                if self.already_have ==False:
                    # ОБЯЗАТЕЛЬНО ПРОКИНУТЬ ОБНОВЛЕНИЕ ПО ВСЕМ ЦЕННАМ 
                    if self.remove == False or self.remove == None:
                        if self.plus_or_minus == None or self.plus_or_minus == True :
                            new_possition = {f'{self.menu_position.id}': 1}
                            each_el[self.client.chat_id][1].append(new_possition)
                            each_el[self.client.chat_id][2] += int(self.menu_position.price)
                            self.update_obj = Object.return_obj(self.client.chat_id,message_id=self.message_id,reply_markup=InlineKeyboardMarkup.update('1',str(self.menu_position.price),menu_id=str(self.menu_position.id),basket_price= str(each_el[self.client.chat_id][2])))
                            Send(main_url,'editMessageReplyMarkup',self.update_obj)
                        #---------adding object if not exists-------

        data_to_read.writting_json(self.json_list,'baskets_json')


    

    def death_time(self):
        self.json_list = data_to_read.reading_json('baskets_json')
        for each_el in self.json_list:
            _, values = zip(*each_el.items())
            values = list(values)[0][0]        
            values = values.split('+')
            date_time_obj = datetime.strptime(values[0], '%Y-%m-%d %H:%M:%S.%f')
            
            date_time_obj = utc.localize(date_time_obj)
            if date_time_obj < datetime.now(utc):
                self.json_list.remove(each_el)
                self.yes_or_not = False
            
        data_to_read.writting_json(self.json_list,'baskets_json')


    @staticmethod
    def create_order_with_phone(chat_id,address,phone):
        json_list = data_to_read.reading_json('baskets_json')
        
        for each_el in json_list:
            print('HERE')
            if str(chat_id) in each_el:
                print('UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
                price = each_el[str(chat_id)][2]
                our_client = Client.query.filter(Client.chat_id == str(chat_id)).first()
                our_client.address = address
                our_client.phone_number = phone
                Commit(our_client)
                new_order = Order(price = int(price),client_id=our_client.id)
                Commit(new_order)
                for i in each_el[str(chat_id)][1]:
                    print(i,'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
                    menu_position, how_many = zip(*i.items())
                    menu_position = list(menu_position)[0]
                    how_many = list(how_many)[0]
                    new_price_list = Price_list(order_id= new_order.id,menu_id =int(menu_position) ,how_many = how_many)   
                    Commit(new_price_list)
    @staticmethod
    def create_order_when_has_all(chat_id):
        json_list = data_to_read.reading_json('baskets_json')
        
        for each_el in json_list:
            print('HERE')
            if str(chat_id) in each_el:
                price = each_el[str(chat_id)][2]
                our_client = Client.query.filter(Client.chat_id == str(chat_id)).first()
                new_order = Order(price = int(price),client_id=our_client.id)
                Commit(new_order)
                for i in each_el[str(chat_id)][1]:
                    print(i,'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
                    menu_position, how_many = zip(*i.items())
                    menu_position = list(menu_position)[0]
                    how_many = list(how_many)[0]
                    new_price_list = Price_list(order_id= new_order.id,menu_id =int(menu_position) ,how_many = how_many)   
                    Commit(new_price_list)
        


    @staticmethod
    def dell(chat_id):
        json_list = data_to_read.reading_json('baskets_json')
        for each_el in json_list:
            if str(chat_id) in each_el:
                json_list.remove(each_el)
        data_to_read.writting_json(json_list,'baskets_json')
    @staticmethod
    def dell_2(chat_id):
        json_list = data_to_read.reading_json('remember_message') 
        for each_el in json_list:
            if str(chat_id) in each_el:
                json_list.remove(each_el)
        data_to_read.writting_json(json_list,'remember_message')
    
            






    
        