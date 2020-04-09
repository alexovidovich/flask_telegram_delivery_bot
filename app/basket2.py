from business.sending import *
from business.object_to_send import *
from business.getting_info import data_to_read
from models import *
from datetime import datetime, timedelta
from business.handler import Menu_obj
from business.sending_key_board import InlineKeyboardMarkup,ReplyKeyboardMarkup
from app import main_url
import os.path
class create_basket_obj:
    @staticmethod
    def create_if_not_exists():
        if not os.path.exists('./static/baskets_json.json'):
            baskets_json = [{'works':'fine'}]
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
class Basket_py(object):
    def __init__(self,client,menu_position,yes_or_not,message_id,plus_or_minus=None,remove=None):
        self.remove = remove
        self.message_id = message_id
        self.client = client
        self.already_have = False
        self.plus_or_minus = plus_or_minus
        self.menu_position = menu_position
        self.yes_or_not = yes_or_not
        self.time = datetime.now(pytz.timezone('Europe/Minsk'))+timedelta(hours=1)
        print(self.remove,self.plus_or_minus)
        if self.yes_or_not == True:
            self.add()
        else:
            self.create()

    def create(self):
        print('CREATE HERE')
        self.json_list = data_to_read.reading_json('baskets_json')
        if self.menu_position.price.isdigit():
            self.price_of_basket = float(self.menu_position.price)
        print(self.price_of_basket,'???????????????????????????????')
        self.personal_basket = {f'{self.client.chat_id}':[str(self.time),[{f'{self.menu_position.id}':1}],self.price_of_basket,[{self.menu_position.id:self.message_id}]]}
        self.json_list.append(self.personal_basket)
        data_to_read.writting_json(self.json_list,'baskets_json')
        # кинуть обновление сообщения для функциии add 
        self.update_obj = Object.return_obj(self.client.chat_id,message_id=self.message_id,reply_markup=InlineKeyboardMarkup.update('1',str(self.menu_position.price),basket_price= str(self.price_of_basket),menu_id=str(self.menu_position.id)))
        #self.update_obj = Object.return_obj(self.client.chat_id,message_id=self.message_id,reply_markup=InlineKeyboardMarkup.lol('works'))
        print(self.update_obj)
        Send(main_url,'editMessageReplyMarkup',self.update_obj)

    def add(self):
        print('ADDDDD HERRERERERE')
        self.json_list = data_to_read.reading_json('baskets_json')
        self.can_add = True
        for each_el in self.json_list:
            if self.client.chat_id in each_el:
                for message in each_el[self.client.chat_id][3]:
        
                    _ , values = zip(*message.items())
                    
                    if int(self.message_id) == int(list(values)[0]):
                        
                        self.can_add = False
                        
                if self.can_add==True:
                    new_dict_in_messages = {self.menu_position.id:self.message_id}
                    each_el[self.client.chat_id][3].append(new_dict_in_messages)

                
                # self.basket_list = each_el[self.client.chat_id][1]
                for possition in each_el[self.client.chat_id][1]:
                    print(possition,self.menu_position.id,type(possition),type(self.menu_position.id))
                    if str(self.menu_position.id) in possition:
                        self.already_have = True
                        print('OLOLOLOLOLOLOLOLOLOLOLOL')
                        if self.plus_or_minus==True:
                            possition[str(self.menu_position.id)]+=1  # нужно будет тут редактировать кол-во + или - в зависимости от колбека
                            each_el[self.client.chat_id][2] += float(self.menu_position.price)     
                        elif self.plus_or_minus==False:
                            if possition[str(self.menu_position.id)]!=1:
                                possition[str(self.menu_position.id)]-=1 
                                each_el[self.client.chat_id][2] -= float(self.menu_position.price)
                                 # нужно будет тут редактировать кол-во + или - в зависимости от колбека
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
                                print(self.pos_menu)
                                print(each_el[self.client.chat_id][1])
                                print(self.pos_menu.id,type(self.pos_menu.id))
                                self.value_of_posit = None
                                for i in each_el[self.client.chat_id][1]:
                                    print(str(self.pos_menu.id),'---------------',i)
                                    if str(self.pos_menu.id) in i:
                                        self.value_of_posit = i[str(self.pos_menu.id)]
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
                            each_el[self.client.chat_id][1].remove(possition)
                        else:
                                #(how_many,price_of_all,price_of_basket,menu_id
                            for i in each_el[self.client.chat_id][3]:
                                self.pos_menu, self.mes_id = zip(*i.items())
                                self.pos_menu =list(self.pos_menu)[0]
                                self.mes_id = list(self.mes_id)[0]
                                self.pos_menu = Menu.query.filter(Menu.id==self.pos_menu).first()
                                print(self.pos_menu)
                                print(each_el[self.client.chat_id][1])
                                print(self.pos_menu.id,type(self.pos_menu.id))
                                for i in each_el[self.client.chat_id][1]:
                                    if str(self.pos_menu.id) in i:
                                        self.value_of_posit = i[str(self.pos_menu.id)]
                                    
                                        
                                        self.update_obj = Object.return_obj(self.client.chat_id,message_id=self.mes_id, \
                                            reply_markup=InlineKeyboardMarkup.update(str(self.value_of_posit ), \
                                                str(float(self.pos_menu.price)*float(self.value_of_posit)), \
                                                    menu_id = str(self.pos_menu.id),basket_price= str(each_el[self.client.chat_id][2])))
                                        Send(main_url,'editMessageReplyMarkup',self.update_obj)
                                    else:
                                        continue
                            
                        
                if self.already_have == False:
                    if self.remove == False or self.remove == None:
                        if self.plus_or_minus == None or self.plus_or_minus == True :
                            new_possition = {f'{self.menu_position.id}': 1}
                            each_el[self.client.chat_id][1].append(new_possition)
                            each_el[self.client.chat_id][2] += int(self.menu_position.price)
                       
                            self.update_obj = Object.return_obj(self.client.chat_id,message_id=self.message_id,reply_markup=InlineKeyboardMarkup.update('1',str(self.menu_position.price),menu_id=str(self.menu_position.id),basket_price= str(each_el[self.client.chat_id][2])))
                            Send(main_url,'editMessageReplyMarkup',self.update_obj)


        data_to_read.writting_json(self.json_list,'baskets_json')


    

    def death_time(self):
        self.json_list = data_to_read.reading_json('baskets_json')
        
        for each_el in self.json_list:
            _, values = zip(*each_el.items())
            values = list(values)
            if values[0] < datetime.now(pytz.timezone('Europe/Minsk')):
                self.json_list.remove(each_el)
            
        data_to_read.writting_json(self.json_list,'baskets_json')






    