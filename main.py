from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from collections import defaultdict #для удобства
from datetime import datetime, timedelta
import re


dictOfSources = {   'cbrf':'https://www.cbr.ru/key-indicators/',
                    'dvbank':'https://www.dvbank.ru/',
                    'selenium':'https://www.selenium.dev/selenium/web/web-form.html'}
'''
todo:
исправить на мягкость поиска денег значения валюты, так как она может быть без точки
'''
# CBRF - res_dict = {CONSTcurrency: {YYYY-MM-DD: float(XX) }
# BANK - res_dict = {CONSTcurrency: {YYYY-MM-DD: {name_address/name_total:{sellBank:XX, buyBank:YY}} } }

def dateFiner(dateVal:str)->str:
    ''' DD.MM.YYYY -> YYYY-MM-DD '''
    sep = ['.']
    if (dateVal[2] in sep) == False or (dateVal[5] in sep) == False or len(dateVal)!=10: return \
        'Wrong separator position or WrongDatePattern'
    for i in sep:
        if i in dateVal:
            return '-'.join(dateVal.split(i)[::-1])

def currencyFiner(amount:str)->float:
    if '.' in amount: #'Xx.yy' -> float(.)
        return float(amount)
    if ',' in amount: # XXX,YYY" -> float(.)
        return float(amount.replace(',','.'))
    try: # xx -> float(xx)
        return float(amount)
    except Exception as err:
        return f'error of amount-pattern / {err}'

    return 'error of amount-pattern'

def parseCbrf(rangeDays = 2,CONSTcurrency = 'USD',)->dict:
    '''
    читаем сводную таблицу
    :param rangeDays: 2==2 or 1
    :return: dict(usd)
    '''
    startParam = ({'url':'https://www.cbr.ru/key-indicators/'}
                  if rangeDays == 2
                  else
                  {'url':'https://www.cbr.ru/currency_base/daily/'})

    driver = webdriver.Chrome()
    driver.get(startParam['url'])
    htmlVar = driver.page_source

    startParam['daysList'] = (
        [ #'-'.join(x.split('.')[::-1])
        dateFiner(x)
         for x
         in re.findall(r"\d{2}\.\d{2}\.\d{4}", htmlVar.split(f'{CONSTcurrency}')[1])[:2:] ]
        #split by currency, gettin values close to currency
        if rangeDays == 2
        else
        [dateFiner(re.findall(r"\d{2}\.\d{2}\.\d{4}",
                             re.findall(r'''data-default-value=[\"\'\.0-9]+''',htmlVar)[0])[0]
                  )]
    )

    res_dict = {CONSTcurrency : {  } }
    for i in startParam['daysList']:
        res_dict[CONSTcurrency][i] = True

    for i in range(len(startParam['daysList'])):
        try:
            res_dict[CONSTcurrency][startParam['daysList'][i]] =  currencyFiner(
                re.findall(r'\d+,\d+',(htmlVar.split('USD')[1]))[:2:][i]
            )
        except Exception as err:
            res_dict[CONSTcurrency][startParam['daysList'][i]] = err

    driver.quit()
    return res_dict

# BANK - res_dict = {CONSTcurrency: {YYYY-MM-DD: {name_address/name_total:{sellBank:XX, buyBank:YY}} } }
def parseDvb(CONSTcurrency = 'USD')->dict:
    # читаем сводную таблицу
    startParam={'url':'https://www.dvbank.ru/'}
    
    driver = webdriver.Chrome()
    driver.get(startParam['url'])
    htmlVar = driver.page_source

    dateVal = dateFiner(
        re.findall(r"\d{2}\.\d{2}\.\d{4}", htmlVar \
        .split('exchange-rates__title-note">')[1])[0])
    res_dict = {CONSTcurrency : {dateVal: {}  }}

    for pos,val in enumerate(['DVB~buy','DVB~sell']):
        try:
            res_dict[CONSTcurrency][dateVal][val] = currencyFiner(re.findall(r'\d+\.\d+',
                                                                             htmlVar.split(CONSTcurrency)[2]\
                                                                             .split('</td'>)[:3:])[pos])
        except Exception as err:
            res_dict[CONSTcurrency][dateVal][val] = err
    return res_dict

def parseSolid(rangeDays = 2,CONSTcurrency = 'USD')->dict:
    # 2==2 or 1
    # api:
    # https://solidbank.ru/api/v1/currency?action=getdata&city=%D0%A5%D0%90%D0%91%D0%90%D0%A0%D0%9E%D0%92%D0%A1%D0%9A&curname=USD&date_from=24.02.2025&date_to=25.02.2025


    startParam = {
        'city' : '%D0%A5%D0%90%D0%91%D0%90%D0%A0%D0%9E%D0%92%D0%A1%D0%9A', #city
        'currency' : CONSTcurrency,
        'leftDate' : str((datetime.today() - timedelta(days = 1))).split(' ')[0],
        'leftDateDot': '.'.join(str(datetime.today() - timedelta(days = 1)).split(' ')[0].split('-')[::-1]),
        'rightDate' : str(datetime.today()),
        'rightDateDot' : '.'.join(str(datetime.today()).split(' ')[0].split('-')[::-1])
    }
    startParam['url'] = ('https://solidbank.ru/api/v1/currency?action=getdata&city='+startParam['city']
                         +'&curname='+startParam['currency']
                         +'&date_from='+startParam['leftDateDot']
                         +'&date_to='+startParam['rightDateDot'])

    startParam['daysList'] = ([str(datetime.today() - timedelta(days = 1)).split(' ')[0],
                               str(datetime.today()).split(' ')[0]][::-1]
        if rangeDays == 2 else
        [str(datetime.today()).split(' ')[0]])

    startParam['daysList'] = ([startParam['leftDateDot'],startParam['rightDateDot']]
        if rangeDays == 2 else
        [startParam['rightDateDot']]
    )

    driver = webdriver.Chrome()
    driver.get(startParam['url'])
    htmlVar = driver.page_source

    res_dict = {CONSTcurrency:{'tempDate':{"SLD~buy":True, "SLD~sell":False}}}
    for i in startParam['daysList']:
        res_dict[CONSTcurrency][dateFiner(i)] = {"SLD~buy":True, "SLD~sell":False}
    del(res_dict[CONSTcurrency]['tempDate'])

    for posDays,valDays in enumerate(startParam['daysList']):
        try:
            buyVal = currencyFiner(
                re.findall(r'\d+\.\d+|\d+', htmlVar.split(valDays)[1])[0]
            )
        except Exception as err: buyVal = err
        try:
            sellVal = currencyFiner(
                re.findall(r'\d+\.\d+|\d+', htmlVar.split(valDays)[1])[1]
            )
        except Exception as err: sellVal = err
        res_dict[CONSTcurrency][dateFiner(valDays)] = {'SLD~buy':buyVal,'SLD~sell':sellVal}

    return res_dict

print("parseSolid(2)",parseSolid(2))

print("parseSolid(66)",parseSolid(66))



