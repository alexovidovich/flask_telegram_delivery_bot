from business.sending import Send
from business.object_to_send import *
from business.getting_info import data_to_read
from models import *
from datetime import datetime, timedelta

from business.sending_key_board import InlineKeyboardMarkup
from app import main_url
class representation:
    @staticmethod
    def repr(data):
        json_list = data_to_read.reading_json('baskets_json')
        repr_list_str=''
        

        how_many = 0
        ssum  = 0
        for each_el in json_list:
            if data['chat_id'] in each_el:
                for possition in each_el[data['chat_id']][1]:
                    keys, values = zip(*possition.items())
                    keys = list(keys)[0]
                    values =list(values)[0]
                    menu_obj= Menu.query.filter(Menu.id == keys).first()


                    el_of_repr =f'{menu_obj.name}-{values}шт.*{menu_obj.price}руб. = {float(values)*float(menu_obj.price)}руб.\n'
                    repr_list_str+= el_of_repr
                    how_many+=float(values)
                    ssum+=float(values)*float(menu_obj.price)

        if repr_list_str == '':

            text=f'Ваш заказ пуст.\n\
Количество товаров:{how_many}. \n\
Итоговая сумма:{ssum}руб.'
            obj = Object.return_obj(data['chat_id'],text = text)
        else:
            text=f'Ваш заказ:\n{repr_list_str}\n\
Количество товаров:{how_many}. \n\
Итоговая сумма:{ssum}руб.'
            obj = Object.return_obj(data['chat_id'],text = text ,reply_markup=InlineKeyboardMarkup.del_basket_or_make_an_order())
            client = Client.query.filter(Client.chat_id==data['chat_id']).first()
            if client.phone_number and client.address:
                text+=f'\n\nАдресс доставки:\n\
{client.address}\n\
Номер телефона для подтверждения заказа:\n\
{client.phone_number}'
                obj = Object.return_obj(data['chat_id'],text = text ,reply_markup=InlineKeyboardMarkup.del_basket_or_make_an_order_or_change())
                        
        Send(main_url,'sendMessage',obj)
    @staticmethod
    def delete(data):
        json_list = data_to_read.reading_json('baskets_json')
        chat_id = data['chat_id']
        for each_dict in json_list:
            if chat_id in each_dict:
                json_list.remove(each_dict)
        data_to_read.writting_json(json_list,'baskets_json')
        text=f'Ваш заказ пуст.\n\
Количество товаров:0шт.\n\
Итоговая сумма:0руб.'
        print(data['message_id'],'0000000000000000000000000000000000000000000')
        update_obj = Object.return_obj(chat_id,text = text ,message_id=data['message_id'],reply_markup=InlineKeyboardMarkup.del_basket_or_make_an_order())
        Send(main_url,'editMessageText',update_obj)


    