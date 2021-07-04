# -*- codeing = utf-8 -*-
# @Time : 2021/4/1 13:02
# @Author : gzk
# @File : testbs4.py
# @Software : PyCharm

import re
def test(html):
    bs = BeautifulSoup(html, 'html.parser')
    # 查找所有a
    # t_list = bs.find_all('a')
    # 正则表达式
    # t_list = bs.find_all(re.compile('a'))    # 标签中含有a字样
    print(t_list)