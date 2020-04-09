from business.interceptor_requests import *
from business.sending import *
from business.sending_key_board import ReplyKeyboardMarkup,InlineKeyboardMarkup
from models import *
from business.object_to_send import Object
from app import main_url
from business.getting_info import data_to_read
import json
import time
class Menu_obj(object):
    @staticmethod
    def menu_obj(name,descr,price):
        descrip = f'{name}\n\
\n\
{descr}\n\
\n\
{price}рублей'
        return descrip
class Handler(object):
    @staticmethod
    def if_start(data):
        method = 'sendMessage'
        for_json =ReplyKeyboardMarkup.creation()
        text=Texts.query.filter(Texts.id == '1').first()
        obj = Object.return_obj(chat_id = data['chat_id'],text=text.hi,reply_markup=for_json)#chat_id,text,photo=None,reply_markup=None,message_id=None
        Send(main_url,method,obj) #url,method_api,obj,*args,**kwargs
    
    @staticmethod
    def if_menu(data):
        begin = time.time()
        if 'call_back' in data:
            if data['call_back']:
                message_id = data['message_id']
                text = data['call_back']
                obj = Object.return_obj(chat_id = data['chat_id'],text=text,message_id=message_id)#chat_id,text,photo=None,reply_markup=None,message_id=None
                Send(main_url,'editMessageText',obj)
                
                begin = time.time()
                method = 'sendPhoto'
                category = Category.query.filter(Category.name == data['call_back']).first()
                menu= Menu.query.filter(Menu.category_id == category.id).all()
                print(time.time()-begin,'00000000000000000000000')
                
                for position in menu:
                    for_json =InlineKeyboardMarkup.creation(position.id)
                    caption = Menu_obj.menu_obj(position.name,position.description,position.price)
                    obj = Object.return_obj(chat_id = data['chat_id'],photo=position.picture,text=caption,reply_markup=for_json)#chat_id,text,photo=None,reply_markup=None,message_id=None
                    Send(main_url,method,obj) #url,method_api,obj,*args,**kwargs
        else:
            method = 'sendMessage'
            text = 'МЕНЮ:'
            for_json =InlineKeyboardMarkup.categories()
            obj = Object.return_obj(chat_id = data['chat_id'],text=text,reply_markup=for_json)#chat_id,text,photo=None,reply_markup=None,message_id=None
            Send(main_url,method,obj) #url,method_api,obj,*args,**kwargs
        
        

    @staticmethod
    def if_any(data):
        ready,address,phone = check.check_if_in_remember_mes(data['chat_id'],data)
        if ready:
            print('READY FOR THE ORDER')
            Basket_py.create_order_with_phone(data['chat_id'],address,phone)
            Basket_py.dell(data['chat_id'])
            Basket_py.dell_2(data['chat_id'])
            text = 'Заявка на заказ создана.Ждите звонка или сообщения для подтверждения заказа.После подтверждения заказ появяится в окне "Заказы".'
            obj = Object.return_obj(data['chat_id'],text)
            Send(main_url,'sendMessage',obj)
    @staticmethod
    def make_ord(data):
            Basket_py.create_order_when_has_all(data['chat_id'])
            Basket_py.dell(data['chat_id'])
            Basket_py.dell_2(data['chat_id'])
            text = 'Заявка на заказ создана.Ждите звонка или сообщения для подтверждения заказа.После подтверждения заказ появяится в окне "Заказы".'
            obj = Object.return_obj(data['chat_id'],text)
            Send(main_url,'sendMessage',obj)

        
            

    



        
        
        
        


    #     @staticmethod
    # def if_menu(data):
    #     begin = time.time()
    #     method = 'sendPhoto'
        
    #     menu= Menu.query.all()
    #     print(time.time()-begin,'00000000000000000000000')
        
    #     for position in menu:
    #         for_json =InlineKeyboardMarkup.creation(position.id)
    #         photo = position.picture
    #         caption = Menu_obj.menu_obj(position.name,position.description,position.price)
    #         obj = Object.return_obj(chat_id = data['chat_id'],photo=position.pict

        
        