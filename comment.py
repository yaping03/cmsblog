__author__ = 'Administrator'
# msg_list = [
#     {'id':1,'content':'xxx','parent_id':None},
#     {'id':2,'content':'xxx','parent_id':None},
#     {'id':3,'content':'xxx','parent_id':None},
#     {'id':4,'content':'xxx','parent_id':1},
#     {'id':5,'content':'xxx','parent_id':4},
#     {'id':6,'content':'xxx','parent_id':2},
#     {'id':7,'content':'xxx','parent_id':5},
#     {'id':8,'content':'xxx','parent_id':3},
# ]
"""
msg_list = [
		{
			'id':1,'content':'xxx',parent_id:None,child:[
				{'id':4,'content':'xxx',parent_id:1},
				{'id':5,'content':'xxx',parent_id:1,child:[
					{'id':7,'content':'xxx',parent_id:5},
				]}]
			},
			{'id':2,'content':'xxx',parent_id:None,child:[
				{'id':6,'content':'xxx',parent_id:2},
			]},
			{'id':3,'content':'xxx',parent_id:None,child:[
				{'id':8,'content':'xxx',parent_id:3},
			]},
	]
"""

# ####################### 前戏 #######################

# v1 = [1,2,3,4]
# v1.append(123)
# print(v1)

# v1 = {'k1':'v1'}
# v1['k2'] = 'v2'
# print(v1)

#
# data = [
#     [11,22,33],
#     [44,55,66]
# ]
#
# data[0].append(data[1])
# # data = [
# #     [11,22,33, [44,55,66]],
# #     [44,55,66]
# # ]
# data[1].append(77)
# # data = [
# #     [11,22,33, [44,55,66]],
# #     [44,55,66,77]
# # ]
# print(data[0][3])

# data = [
# 	{'k1':'v1'},
# 	{'k2':'v2'}
# ]
#
# for item in data:
# 	item['kk'] = 'vv'
#
# print(data)




msg_list = [
    {'id':1,'content':'xxx','parent_id':None},
    {'id':2,'content':'xxx','parent_id':None},
    {'id':3,'content':'xxx','parent_id':None},
    {'id':4,'content':'xxx','parent_id':1},
    {'id':5,'content':'xxx','parent_id':4},
    {'id':6,'content':'xxx','parent_id':2},
    {'id':7,'content':'xxx','parent_id':5},
    {'id':8,'content':'xxx','parent_id':3},
]

# v = [row.setdefault('child',[]) for row in msg_list]
# print(msg_list)
# msg_list_dict = {
#
# }
#
# for item in msg_list:
# 	item['child'] = []
# 	msg_list_dict[item['id']] = item
#
# # #### msg_list_dict用于查找,msg_list
# result = []
# for item in msg_list:
# 	pid = item['parent_id']
# 	if pid:
# 		msg_list_dict[pid]['child'].append(item)
# 	else:
# 		result.append(item)

# result就是最后结果

# #########################
"""
1.终端显示
2.Djangoview函数中python显示
3.js代码 ***
评论1
    评论4
		评论6
	评论5
评论2
评论3
"""

import requests

requests.post(
	url='http://127.0.0.1:8000/wangzhe.html',
	data={
		'username':'xxxxxxxx'
	}
)


