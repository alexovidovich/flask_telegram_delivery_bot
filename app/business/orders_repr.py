from models import * 
from business.sending import *
from business.object_to_send import *
from app import main_url
class Repr:
    @staticmethod
    def represent(data):
        my_client = Client.query.filter(Client.chat_id == data['chat_id']).first()
        his_orders = Order.query.filter(Order.client_id == my_client.id).filter(Order.status == True).all()
        number=0
        if len(his_orders)==0:
            text=f'У вас не было еще ни одного заказа.'
            obj = Object.return_obj(data['chat_id'],text=text)
            Send(main_url,method_api = 'sendMessage',obj=obj)


        for each_order in his_orders:
            number +=1 
            order_positions = Price_list.query.filter(Price_list.order_id == each_order.id).all()


            repr_list_str=''
            for each_position in order_positions:
                position = Menu.query.filter(Menu.id == each_position.menu_id).first()
                el_of_repr =f'{position.name}-{each_position.how_many}шт.*{position.price}руб. = {float(each_position.how_many)*float(position.price)}руб.\n'
                repr_list_str+= el_of_repr
            

            text=f'Заказ №{str(number)}:\n{repr_list_str}\n \
Количество товаров:{str(len(order_positions))}. \n \
Итоговая сумма:{str(each_order.price)}руб.'

            obj = Object.return_obj(data['chat_id'],text=text)
            Send(main_url,method_api = 'sendMessage',obj=obj)




