# -*- coding: UTF-8 -*-

import re
import json

# 数据输入
text = input()
target = text[0]
# 提取姓名
name = re.search(r'\w+(?=,)', text).group()
# 提取电话号码
phone_number = re.search(r'\d{11}', text).group()
#  clear
text = text.replace(phone_number, '')
text = text.replace(".", "")
index = text.find(',')
index = index + 1
text = text[index:]
# 提取地址
pattern = re.compile(r'(?P<province>[^省]+自治区|.*?省|.*?行政区|)(?P<city>[^市]+自治州|.*?地区|.*?行政单位|.+盟|市辖区|.*?市|)(?P<county>[^县]+县|.+?区|.+市|.+旗|.+海域|.+岛)?(?P<town>.+镇|.+街道)?(?P<road>.*街|.*路|.*巷)?(?P<number>\d+号|)?(?P<village>.*)')
province = None 
city = None
county = None
town = None
road = None
number = None
village = None
## 一级地址,二级地址比对表
list1 = []
list2 = []
with open('Adress', 'r', encoding='utf-8') as f:
    for line in f:
        num = re.search(r'\b\d{6}\b', line).group()
        cha = re.search(r'\b[\u4e00-\u9fa5]+\b', line).group()
        if(num[2:6] == '0000'):
            list1.append(cha)
        elif (num[4:6] == '00'):        
            list2.append(cha)

## 比对地址
array = []
m = pattern.search(text)
if m:
    ### 一级地址
    if(m.group('city') == '北京市' or m.group('city') == '上海市' or m.group('city') == '重庆市' or m.group('city') == '天津市'):
        cha = m.group('city')
        array.append(cha[0 : len(cha) - 1])
    else:
        province = m.group('province') if m.group('province') else ''
        if province == '':
            for s in list1 :
                if s[0:2] == text[0:2]:
                    province = s
                    if province[-1] == '省':
                        text = text[len(province) -1 :]
                    if province[-3::] == '自治区':
                        text = text[len(province) -3 :]
                    if province[-3::] == '行政区':
                        text = text[len(province) -3 :]
        array.append(province) 
    ### 二级地址
    m = pattern.search(text)
    if m:
        city = m.group('city') if m.group('city') else ''
        if city == '':
            for s in list2:
                if s[0:2] == text[0:2]:
                    city = s
                    if city[-1] == '市':
                        text = text[len(city) -1 :]
                    elif city[-3:] == '自治州':
                        text = text[len(city) -3 :]
        array.append(city) 
    ### 三级及三级以下地址
    m = pattern.search(text)
    if m:
        county = m.group('county') if m.group('county') else ''
        town = m.group('town') if m.group('town') else ''
        road = m.group('road') if m.group('road') else ''
        number = m.group('number') if m.group('number') else ''
        village = m.group('village') if m.group('village') else ''
        array.append(county) 
        array.append(town) 
        if target == '1':
            array.append(road + number + village) 
        else:
            array.append(road) 
            array.append(number) 
            array.append(village)
# 输出json
mydict = {'姓名': name,  '手机': phone_number, '地址': array}
answer = []
answer.append(mydict)
f = json.dumps(answer)
print(f)

# try:
#     with open('data.json', 'w', encoding='utf-8') as fs:
#         json.dump(mydict, fs)
# except IOError as e:
#     print(e)
# print('保存数据完成!')


'''
1!小陈,广东省东莞市凤岗13965231525镇凤平路13号.                     
1!张三,福建福州闽13599622362侯县上街镇福州大学10#111.
2!王五,福建省福州市鼓楼18960221533区五一北路123号福州鼓楼医院.
2!李四,福建省福州13756899511市鼓楼区鼓西街道湖滨路110号湖滨大厦一层.  
3!小美,北京市东15822153326城区交道口东大街1号北京市东城区人民法院.
'''