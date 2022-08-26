import requests


def get_current_bill(fields):
    ### 获取公司当前的资产负债情况
    stock_dict = dict()
    url = 'http://27.push2.eastmoney.com/api/qt/clist/get'
    for i in range(1, 10):
        if fields is None:
            fields = 'f2,f12'
        data = {
            'fields': fields,
            'pz': 1000,  # 每页条数
            'pn': i,  # 页码
            'fs': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048'
        }
        response = requests.get(url, data)
        response_json = response.json()
        # print(i, response_json)
        # 返回数据为空时停止循环
        if response_json['data'] is None:
            break
        for j, k in response_json['data']['diff'].items():
            code = k['f12']  # 代码
            # name = k['f14']  # 名称
            # price = k['f2']  # 股价
            # pe = k['f9']  # 动态市盈率
            # pb = k['f23']  # 市净率
            industry = k['f100'] #行业
            print('hangye',industry)
            # total_value = k['f20']  # 总市值
            # currency_value = k['f21']  # 流通市值
            # price = round(price / 100, 2)  # 价格转换为正确值（保留2位小数）
            # pe = round(pe / 100, 2)  # 市盈率转换为正确值（保留2位小数）
            # pb = round(pb / 100, 2)  # 市净率转换为正确值（保留2位小数）
            # total_value = round(total_value / 100000000, 2)  # 总市值转换为亿元（保留2位小数）
            # currency_value = round(currency_value / 100000000, 2)  # 流通市值转换为亿元（保留2位小数）
            stock_dict[code] = k


    return stock_dict



dict_ = dict()
list_ = list()
with open('标号含义对应表.txt','r',encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(':')
        print(line)

        dict_[line[0]] = line[1]
        list_.append(line[0])

fields = ','.join(list_)
get_current_bill(fields)



