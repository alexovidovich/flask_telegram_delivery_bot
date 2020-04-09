from business.getting_info import data_to_read
import requests 
import time


class Send(object):
    def __init__(self,url,method_api,obj,*args,**kwargs):
        self.url = url
        self.method_api = method_api
        self.obj = obj
        self.list = args
        self.dict = kwargs
        self.send()
    def send(self):
        self.route = self.url + self.method_api
        print(self.route,self.obj,type(self.obj['chat_id']),type(self.route))
        begin = time.time()
        print('start sanding')
        sending_info = requests.post(self.route,json=self.obj)
        print('sent')
        print(time.time()-begin)
        
       
