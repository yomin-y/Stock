import pandas as pd
import requests




def gen_secid(stock_code: str) -> str:
    '''
    生成东方财富专用的secid

    Parameters
    ----------
    stock_code: 6 位股票代码

    Return
    ------
    str : 东方财富给股票设定的一些东西
    '''
    # 沪市指数
    if stock_code[:3] == '000':
        return f'1.{stock_code}'
    # 深证指数
    if stock_code[:3] == '399':
        return f'0.{stock_code}'
    # 沪市股票
    if stock_code[0] != '6':
        return f'0.{stock_code}'
    # 深市股票
    return f'1.{stock_code}'


def get_history_bill(stock_code: str) -> pd.DataFrame:
    '''
    获取多日单子数据
    -
    Parameters
    ----------
    stock_code: 6 位股票代码

    Return
    ------
    DataFrame : 包含指定股票的历史交易日单子数据（大单、超大单等）

    '''
    EastmoneyHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
    EastmoneyBills = {
        'f51': '日期',
        'f52': '开盘价',
        'f53': '收盘价',
        'f54': '最高价',
        'f55': '最低价',
        'f56': '振幅',
        'f57': '总交易手数',
        'f58': '总交易金额',
        'f59': '涨跌幅',
        'f60': '涨跌额',
        'f61': '换手率',

    }
    fields = list(EastmoneyBills.keys())
    columns = list(EastmoneyBills.values())
    fields2 = ",".join(fields)
    secid = gen_secid(stock_code)
    params = (
        ('lmt', '100000'),
        ('klt', '101'),
        ('fqt', '1'),
        ('secid', secid),
        ('fields1', 'f1,f2,f3,f4,f5,f6,f7'),
        ('fields2', fields2),
        ('beg', '0'),
        ('end', '20500000')

    )
    params = dict(params)
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    json_response = requests.get(url,
                                 headers=EastmoneyHeaders,params=params).json()
    data = json_response.get('data')
    if data is None:
        if secid[0] == '0':
            secid = f'1.{stock_code}'
        else:
            secid = f'0.{stock_code}'
        params['secid'] = secid

        json_response: dict = requests.get(
            url, headers=EastmoneyHeaders, params=params).json()
        data = json_response.get('data')
    if data is None:
        print('股票代码:', stock_code, '可能有误')
        return pd.DataFrame(columns=columns)
    if json_response is None:
        return
    data = json_response['data']
    klines = data['klines']
    rows = []
    for _kline in klines:
        kline = _kline.split(',')
        rows.append(kline)
    df = pd.DataFrame(rows, columns=columns)

    return df


if __name__ == "__main__":

    # stock_code = '601258'
    # # 调用函数获取股票历史单子数据（有天数限制）
    # df = get_history_bill(stock_code)
    # # 保存数据到 csv 文件中
    # df.to_csv(f'data\\{stock_code}.csv', index=None, encoding='utf-8-sig')
    # print(stock_code, f'的历史单子数据已保存到文件 {stock_code}.csv 中')


    # 股票代码
    stock_codes_file = open('stock_codes.csv','r',encoding='utf-8')
    stock_codes = stock_codes_file.readlines()
    for idx, stock_code in enumerate(stock_codes):
        if idx ==0:
            continue #去掉表头

        stock_code = stock_code.strip().split(',')[1]

        # 调用函数获取股票历史单子数据（有天数限制）
        df = get_history_bill(stock_code)
        # 保存数据到 csv 文件中
        df.to_csv(f'data\\{stock_code}.csv', index=None, encoding='utf-8-sig')
        print(stock_code, f'的历史单子数据已保存到文件 {stock_code}.csv 中')
    stock_codes_file.close()