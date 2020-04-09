import json
from flask import request




class data_to_read(object):

    @classmethod
    def getting_info(cls):
        if request.method == 'POST':
            data = request.get_json()
            return data


    @classmethod
    def mapping_info_user(cls,comming_data=None):
        data = comming_data or cls.reading_json(name = 'json_api_update')
        print(data,'DAAAAATTTAA')
        if data!=None:
            dict_data = {}
            if 'callback_query' in data:
                data = data['callback_query']
                dict_data['call_back']=cls.check('data',data)
            dict_data['teleg_id']=cls.check('username',data['message']['from'])
            dict_data['message_id']=cls.check('message_id',data['message'])
            dict_data['name']=cls.check('first_name',data['message']['from'])
            dict_data['chat_id']=str(cls.check('id',data['message']['chat']))
            dict_data['text']=cls.check('text',data['message'])
            if 'photo' in data['message']:
                dict_data['photo']=cls.check('photo',data['message'])[-1]['file_id']
                dict_data['caption']=cls.check('caption',data['message'])
            print(dict_data)

            
            return dict_data
       
    @classmethod
    def check(cls,x:str,route):
        
        if x in route:
            back = route[x]
            
        else:
            back = None
        return back

    @staticmethod
    def writting_json(data,name):
        with open(f'./static/{name}.json','w',encoding='utf-8') as f:
            json.dump(data,f,indent=2,ensure_ascii=False) 
    @classmethod
    def reading_json(cls,name):
        with open(f'./static/{name}.json','r',encoding='utf-8') as f:
            data = json.load(f)
        return data
    @staticmethod
    def add_json(data,name):
        with open(f'./static/{name}.json','a',encoding='utf-8') as f:
            json.dump(data,f,indent=2,ensure_ascii=False) 
    
            