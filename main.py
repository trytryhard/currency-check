from selenium import webdriver
from datetime import datetime, timedelta
import time
import re
import pandas as pd

from finer import dateFiner, currencyFiner


'''
todo:
chapter X:
    sberbank;
    ??

chapter XX:
    aggregate data  
'''
# CBRF - res_dict = {CONSTcurrency: {YYYY-MM-DD: float(XX) }
# BANK - res_dict = {CONSTcurrency: {YYYY-MM-DD: {name_address/name_total:{sellBank:XX, buyBank:YY}} } }


def parseCbrf(rangeDays = 2,CONSTcurrency:str = 'USD',)->dict:
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
def parseDvb(CONSTcurrency:str = 'USD')->dict:
    # читаем сводную таблицу
    startParam={'url':'https://www.dvbank.ru/'}
    
    driver = webdriver.Chrome()
    driver.get(startParam['url'])
    htmlVar = driver.page_source

    dateVal = dateFiner(
        re.findall(r"\d{2}\.\d{2}\.\d{4}", htmlVar \
        .split('exchange-rates__title-note">')[1])[0])
    res_dict = {CONSTcurrency : {dateVal: {}  }}

    for num,i in enumerate(htmlVar.split(CONSTcurrency)[2].split('</td>')[1:3:]):
        print(num,i)
        print(currencyFiner(i.split('</span>')[1]))

    for pos,val in enumerate(['DVB~buy','DVB~sell']):
        try:
            res_dict[CONSTcurrency][dateVal][val] = currencyFiner(htmlVar\
                                                                  .split(CONSTcurrency)[2]\
                                                                  .split('</td>')[1:3:][pos]\
                                                                  .split('</span>')[1])
        except Exception as err:
            res_dict[CONSTcurrency][dateVal][val] = err
    return res_dict

def parseSolid(rangeDays = 2,CONSTcurrency:str = 'USD')->dict:
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

    res_dict = {CONSTcurrency:{'tempDate':{"SLD~buy":None, "SLD~sell":None}}}
    for i in startParam['daysList']:
        res_dict[CONSTcurrency][dateFiner(i)] = {"SLD~buy":None, "SLD~sell":None}
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

def parseVTB(CONSTcurrency:str = 'USD')->dict:
    '''
    api: https://www.vtb.ru/api/currencyrates/table?category=1&type=1
    :param CONSTcurrency:
    :return: res_dict
    '''
    startParam = {
        'url' : 'https://www.vtb.ru/api/currencyrates/table?category=1&type=1',
        'currency' : CONSTcurrency
    }

    driver = webdriver.Chrome()
    driver.get(startParam['url'])
    htmlVar = driver.page_source
    startParam['dateVal'] = re.findall(r'\d+\-\d+\-\d+',htmlVar)[0]
    res_dict = {CONSTcurrency: {startParam['dateVal']: {"VTB~buy": None, "VTB~sell": None}}}

    for pos,val in enumerate(['VTB~buy','VTB~sell']):
        try:
            res_dict[CONSTcurrency][startParam['dateVal']][val] = (
                currencyFiner(
                    re.findall(r'\d+\.\d+',htmlVar.split(CONSTcurrency)[1].split('Российский рубль')[1])[pos]
                )
            )
        except Exception as err:
            res_dict[CONSTcurrency][startParam['dateVal']][val] = err

    return res_dict

def parseSber(rangeDays = 2,CONSTcurrency:str = 'USD') ->dict:
    startParam = {
        'url_default' : 'https://www.sberbank.ru/ru/quotes/currencies?tab=vsp&currency=USD',
        'region':'070',
        'url':'https://www.sberbank.ru/proxy/services/rates/public/graph?rateType=ERNP-1&isoCode=USD&regionId=070&id=4480470314&dateBeg=1737925200000&dateEnd=1740603600001&segType=TRADITIONAL',
        'currency' : CONSTcurrency,
        'rightDate':int(datetime.now().timestamp())*10**3
    }
    # TODO : нужно добавить словарь регион-код (достать из хендшейков сбера) ~ для regionId выручит
    #const c = `/proxy/services/rates/public/graph?rateType=${e}&isoCode=${t}&regionId=${r}&id=4480470314&dateBeg=${o}&dateEnd=${i}&segType=TRADITIONAL`;

    startParam['leftDate'] = startParam['rightDate'] - 24*60*60*10**3 if rangeDays == 2 else startParam['rightDate']

    startParam['url'] = f'''https://www.sberbank.ru/proxy/services/rates/public/graph?rateType=ERNP-1&isoCode={startParam["currency"]}&regionId={startParam["region"]}&id=4480470314&dateBeg={startParam["leftDate"]}&dateEnd={startParam["rightDate"]}&segType=TRADITIONAL'''

    print(startParam['url'])

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)

    driver.get(startParam['url'])
    time.sleep(6) #5 - works || rework with fine waiter no time.sleep ^_^

    htmlVar = driver.page_source
    print(htmlVar)
    res_dict = {CONSTcurrency: {'bulk': {"Sber~buy": None, "Sber~sell": None}}}

    for i in htmlVar.split(CONSTcurrency)[1].split('}]}')[::-1]:
        if re.findall('\d{13}',i)  == []: continue
        else: dateVal = dateFiner(re.findall('\d{13}',i)[0])
        sberBuy = currencyFiner(re.findall(r'\d+\.\d+|\d+',re.findall(r'rateBuy":\d+\.\d+|rateBuy":\d+',i)[0])[0])
        sberSell = currencyFiner(re.findall(r'\d+\.\d+|\d+',re.findall(r'rateSell":\d+\.\d+|rateSell":\d+',i)[0])[0])
        res_dict[CONSTcurrency][dateVal] = {"Sber~buy":sberBuy,"Sber~sell":sberSell }
    del res_dict[CONSTcurrency]['bulk']
    return res_dict

#def getActualPdFrame(d:dict)->pd.DataFrame:


#def parseData():


print("parseSber()",parseSber(1))

#print("parseSolid(66)",parseSolid(66))

