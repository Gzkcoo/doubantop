# -*- codeing = utf-8 -*-
# @Time : 2021/4/1 11:16
# @Author : gzk
# @File : testUrllib.py
# @Software : PyCharm


import urllib.request


# 获取一个Get请求
# response = urllib.request.urlopen('http://www.baidu.com')
# print(response.read().decode('utf-8'))

# import urllib.parse
# # 获取一个Post请求
# data = bytes(urllib.parse.urlencode({'hello': 'world'}), encoding='utf-8')
# response = urllib.request.urlopen('http://httpbin.org/post', data=data)
# print(response.read().decode('utf-8'))

# import urllib.parse
# headers = {
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
# }
# data = bytes(urllib.parse.urlencode({'name': 'Jenny'}), encoding='utf-8')
# url = 'http://httpbin.org/post'
# req = urllib.request.Request(url, data=data, headers=headers, method='POST')
# response = urllib.request.urlopen(req)
# print(response.read().decode('utf-8)'))


url = 'http://www.douban.com'
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
req = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))