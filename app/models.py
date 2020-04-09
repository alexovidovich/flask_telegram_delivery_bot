from app import *
from datetime import datetime, timedelta
import pytz

# default=datetime.now(pytz.timezone('Europe/Minsk'))+timedelta(hours=1,minutes=30)

class Commit:
    def __init__(self,obj=None,objs=None):
        self.obj=obj
        self.objs=objs
        if self.obj:
            db.session.add(self.obj)
        elif self.objs:
            db.session.add_all(self.objs)
        db.session.commit()



class Client(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    teleg_id = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    name = db.Column(db.String(50))
    chat_id = db.Column(db.String(10),unique=True)
    address = db.Column(db.String(300))
    orders = db.relationship('Order', backref='client', lazy=True)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class Order(db.Model):#заказ 
    id = db.Column(db.Integer,primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'),
        nullable=False)
    active = db.Column(db.Boolean(), unique=False,default=True)# true - заказ отклонен false -просто неподтвержден 
    date = db.Column(db.DateTime)
    price_list = db.relationship('Price_list', backref='order', lazy=True)
    status = db.Column(db.Boolean(), unique=False,default=False)#0 -неподтвержден, 1 -подтвержден # принятые заказы и новые заказы 
                                                                                                                        # подтвердить заказ 
                                                                                                                        # отклонить заказ 
                                                                                                                            
    
    time_of_delivery = db.Column(db.DateTime)
    price = db.Column(db.Integer)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class Menu(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'),
        nullable=False)
    price_list  = db.relationship('Price_list', backref='menu', lazy=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    picture = db.Column(db.String(300))
    active = db.Column(db.Boolean(),default = True)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #заказ       id  order    menu_position     how_many    
#                         #             1    6           23               3
#                         #             2    6           43               2
                            #           3    8           23               1
class Price_list(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    order_id =db.Column(db.Integer,db.ForeignKey('order.id'),
        nullable=False)
    menu_id =db.Column(db.Integer,db.ForeignKey('menu.id'),
        nullable=False) 
    how_many = db.Column(db.Integer)
class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    menu =db.relationship('Menu',backref = 'category',lazy = True)


class Texts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text)
    description = db.Column(db.String(100))


