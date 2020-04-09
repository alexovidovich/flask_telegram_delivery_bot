class Object:
    
    @classmethod
    def return_obj(cls,chat_id,text=None,photo=None,reply_markup=None,message_id=None):
        
        obj = {'chat_id': chat_id}
        if photo:
            obj['photo']=photo
            obj['caption'] = text
        elif text:
            obj['text']=text
        


        if reply_markup:
            obj['reply_markup']=reply_markup
        if message_id:
            obj['message_id']=message_id

        return obj
