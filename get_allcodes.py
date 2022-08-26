import re
import requests
import json
import pandas as pd

def submit_website(num,psize):
    start_url = "http://43.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112409654478365018256" \
                "_1661501814311&pn=%d&pz=%d&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|" \
                "web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&" \
                "fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1661501814401" %(num,psize)
    headers = {"User-Agent": ":Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"}

    response = requests.get(start_url, headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')

def return_data(num,psize):
    html = submit_website(num,psize)
    p = re.compile(r'[(](.*?)[)]')
    result = re.findall(p, html)
    myjson=json.loads(result[0])
    return myjson['data']['diff']

def get_stock_list(num,psize):
    # 得到股票代码的列表
    stock_list=[x['f12'] for x in return_data(num,psize)]
    return stock_list

stock_list=[]
for i in range(1,12):
    stock_codes=get_stock_list(i,500) #每页取500个股票数据,10页就够了。
    stock_list+=stock_codes

stock_codes=pd.DataFrame(stock_list,columns=['股票代码'])
stock_codes.to_csv('F:\\stock\\stock_codes.csv') #保存为”股票列表.csv”文件