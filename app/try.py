import time,re 
start = time.time()
k = '{"пирог":"3"},{"кекс":"2"},{"вода":"6"},{"супы":"3"}'
list_ = k.split(',')
list2 = []
list3 = []
for i in list_:
    dict_ = eval(i)
    list2.append(dict_)
for i in list2:
    keys, values = zip(*i.items())
    keys = list(keys)
    values = list(values)
   
    summ = keys+values
    list3.append(summ)

    # выдача инфы по 1 позиции что именно i[0]
    # выдача кол-ва штук i[1]

print(list3,time.time()-start)

k = {'3242342':['3234',[{'2':'3'}]]}
keys, values = zip(*k.items())
keys = list(keys)
values = list(values)
print(keys,values)
print(type(keys),type(values))





# client-OBJ,menu_position-OBJ,yes_or_not-TRUE,FALSE 

menu_position_id = '5'


my_list = [{'2':'3'},{'3':'3'},{'1':'5'},{'4':3},{'6':'8'}]
for i in my_list:
    if menu_position_id in i:
        print('its here')
d = u'[г.Минск ул.Маяковского д.438 кв.320]'
o =re.compile(u'(\w+')
k = re.findall(o,d) 
print(k)
Описание: свежая кошечка, политая нежными солнечными лучами, с терпким ароматом молодой мягкой шерсти. Торчащие нежные усики сделают ощущения незабываемыми. Подается слегка теплым. 
AgACAgIAAxkBAAIEaF6EbQl0T1dJo2HznkBoYXxXLKa3AALTrjEbPZ4AAUgM3yeEOsfi0T9rTJEuAAMBAAMCAAN5AAOvwgEAARgE
4 сыра
AgACAgIAAxkBAAIEbl6EbcvMakIYjxY4gpYcvZfPKG0WAAKyrDEbQkcgSMbTjnp26ChjS4LBDwAEAQADAgADdwADfTsGAAEYBA
вишневый
AgACAgIAAxkBAAIEbV6EbbjXyL7sRFiHBm6RqlnCDH0yAAKxrDEbQkcgSA8EZ7cpmt8VGnrBDwAEAQADAgADeAADazAGAAEYBA

Добрый день!  Приветствуем вас в чат-боте LIFOOD.  LIFOOD- это сеть сбалансированного питания. Нажмите кнопку "меню", чтобы увидеть все категории.

DELETE FROM `bot_tel`.`order_client` WHERE `order_id`='1';

DELETE FROM `bot_tel`.`order` WHERE `id`='1';

