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
цбр - курс находится в рамках индикаторов
двбанк - курс на главной странице 
сбер - в рамках карты
'''
# CBRF - res_dict = {CONSTcurrency: {YYYY-MM-DD: float(XX) }
# BANK - res_dict = {CONSTcurrency: {YYYY-MM-DD: {address/total:{sellBank:XX, buyBank:YY}} } }

def dateFiner(dateVal:str)->str:
    ''' DD.MM.YYYY -> YYYY-MM-DD '''
    sep = ['.']
    if (dateVal[2] in sep) == False or (dateVal[5] in sep) == False or len(dateVal)!=10: return 'WrongDatePattern'
    for i in sep:
        if i in dateVal:
            return '-'.join(dateVal.split(i)[::-1])

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


    usd = defaultdict(float)

    res_dict = {CONSTcurrency : {  } }
    for i in startParam['daysList']:
        res_dict[CONSTcurrency][i] = True


    for i in range(len(startParam['daysList'])):
        try:
            res_dict[CONSTcurrency][startParam['daysList'][i]] =  (
                float(re.findall(r'\d+,\d+',(htmlVar.split('USD')[1]))[:2:][i]\
                .replace(',','.'))
            )
        except Exception as err:
            res_dict[CONSTcurrency][startParam['daysList'][i]] = err

    driver.quit()
    return res_dict

def parseDvb()->dict:
    # читаем сводную таблицу
    startParam={'url':'https://www.dvbank.ru/'}
    
    driver = webdriver.Chrome()
    driver.get(startParam['url'])
    htmlVar = driver.page_source

    usd = defaultdict(float)

    usd['valid_date'] = '-'.join(
        re.findall(r"\d{2}\.\d{2}\.\d{4}", htmlVar \
        .split('exchange-rates__title-note">')[1])[1]\
        .split('.')[::-1])

    for pos,val in enumerate(['buyBank','sellBank']):
        try:
            # 2 так как тут лежит фантомная таблица ??
            usd[val] = re.findall(r'\d+\.\d+', htmlVar.split('1$)')[2])[pos]
        except Exception as err: usd[val]=err
    return usd

def parseSolid(rangeDays = 2)->dict:
    # 2==2 or 1
    # читаем графы
    #startParam = {'url': 'https://solidbank.ru/currency-transactions/'}
    #driver = webdriver.Chrome()
    #driver.get(startParam['url'])

    startParam = {
        'city' : '%D0%A5%D0%90%D0%91%D0%90%D0%A0%D0%9E%D0%92%D0%A1%D0%9A', #city
        'currency' : 'USD',
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

    driver = webdriver.Chrome()
    driver.get(startParam['url'])
    htmlVar = driver.page_source


    usd = {}

    for i in range(len(startParam['daysList'])):
        try:
            buyBank =  re.findall('\d+\.\d+',htmlVar.split('UF_DATE')[-1-i])[1]
            sellBank = re.findall('\d+\.\d+',htmlVar.split('UF_DATE')[-1-i])[2]
            usd[startParam['daysList'][i]] = ['sellBank=',sellBank,'buyBank=',buyBank]
        except Exception as err: usd[startParam['daysList'][i]] = err




    return usd
print(parseCbrf(2))
print(parseCbrf(66))


