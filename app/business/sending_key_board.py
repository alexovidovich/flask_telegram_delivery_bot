from models import *
import json
class ReplyKeyboardMarkup:
    

    @staticmethod
    def creation():
        keyboard= [[{'text':'Меню'},{'text':'Корзина'}],[{'text':'Заказы'},{'text':'Помощь'}]]
        not_ready = {'keyboard': keyboard ,'resize_keyboard':True}
        ready = json.dumps(not_ready)
        return ready
    
class InlineKeyboardMarkup:
    
    @staticmethod
    def creation(name:str):
        keyboard= [[{'text':'Добавить в корзину','callback_data':name}]]
        not_ready = {'inline_keyboard': keyboard }
        ready = json.dumps(not_ready)
        return ready
    
    
    #для обновления новый метод
    @staticmethod
    def update(how_many,price_of_all,menu_id,basket_price):
        keyboard= [[{'text':f'{how_many}шт. - {price_of_all}руб','callback_data':'None'}],[{'text':'Убрать','callback_data':f'{menu_id},delete_this_position'},{'text':'-1','callback_data':f'{menu_id},reduce'},{'text':'+1','callback_data':f'{menu_id},increase'}],[{'text':f'заказ на {basket_price} руб. Оформить?','callback_data':f'{menu_id},activate'}]]
        not_ready = {'inline_keyboard': keyboard }
        ready = json.dumps(not_ready)
        return ready
    
   
    @staticmethod
    def del_basket_or_make_an_order():
        keyboard= [[{'text':'Очистить корзину','callback_data':'clean'}],[{'text':'Сделать заказ','callback_data':'getaddress'}]]
        not_ready = {'inline_keyboard': keyboard }
        ready = json.dumps(not_ready)
        return ready
    @staticmethod
    def del_basket_or_make_an_order_or_change():
        keyboard= [[{'text':'Очистить корзину','callback_data':'clean'}],[{'text':'Сделать заказ','callback_data':'make_order'}],[{'text':'Исправить данные доставки','callback_data':'getaddress'}]]
        not_ready = {'inline_keyboard': keyboard }
        ready = json.dumps(not_ready)
        return ready
    @staticmethod
    def categories():
        categories = Category.query.all()
        keyboard= []
        for each_category in categories:
            new_category = [{'text':f'{each_category.name}','callback_data':f'{each_category.name}'}]
            keyboard.append(new_category)
        not_ready = {'inline_keyboard': keyboard }
        ready = json.dumps(not_ready)
        return ready

# [{'text':f'заказ на {price_of_basket} руб. Оформить?','callback_data':f'{menu_id},activate'}]