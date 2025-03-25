from selenium import webdriver
from datetime import datetime, timedelta, date
import time
import re
from finer import  DateFiner, CurrencyFiner
# need to rewrite finer to classes

class BankBluePrint:
    url = None
    currency = None

    extraCity = None
    extraLeftDate = None
    extraRightDate = None

    def twoDays(self):
        pass
    def oneDay(self):
        pass
    '''
    1)oneDay get info from twoDays and return last-actual date
    2)if no twoDays info, so it return oneDay with NONe in previous day 
    '''

class CentralBankOfTheRF:
    url = f'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To='
    currencyDict = {
        'AUD': ['Australian Dollar', 1],
        'AZN': ['Azerbaijan Manat', 1],
        'AMD': ['Armenian Dram', 100],
        'THB': ['Baht', 10],
        'BYN': ['Belarusian Ruble', 1],
        'BGN': ['Bulgarian Lev', 1],
        'BRL': ['Brazilian Real', 1],
        'KRW': ['Won', 1000],
        'HKD': ['Hong Kong Dollar', 1],
        'UAH': ['Hryvnia', 10],
        'DKK': ['Danish Krone', 1],
        'AED': ['UAE Dirham', 1],
        'USD': ['US Dollar', 1],
        'VND': ['Dong', 10000],
        'EUR': ['Euro', 1],
        'EGP': ['Egyptian Pound', 10],
        'PLN': ['Zloty', 1],
        'JPY': ['Yen', 100],
        'INR': ['Indian Rupee', 10],
        'CAD': ['Canadian Dollar', 1],
        'QAR': ['Qatari Rial', 1],
        'GEL': ['Lari', 1],
        'MDL': ['Moldovan Leu', 10],
        'NZD': ['New Zealand Dollar', 1],
        'TMT': ['Turkmenistan New Manat', 1],
        'NOK': ['Norwegian Krone', 10],
        'RON': ['Romanian Leu', 1],
        'IDR': ['Rupiah', 10000],
        'ZAR': ['Rand', 10],
        'XDR': ['SDR (Special Drawing Right)', 1],
        'RSD': ['Serbian Dinar', 100],
        'SGD': ['Singapore Dollar', 1],
        'KGS': ['Som', 10],
        'TJS': ['Somoni', 10],
        'KZT': ['Tenge', 100],
        'TRY': ['Turkish Lira', 10],
        'UZS': ['Uzbekistan Sum', 10000],
        'HUF': ['Forint', 100],
        'GBP': ['Pound Sterling', 1],
        'CZK': ['Czech Koruna', 10],
        'SEK': ['Swedish Krona', 10],
        'CHF': ['Swiss Franc', 1],
        'CNY': ['Yuan Renminbi', 1]
    }

    def __init__(self, curr='USD'):
            self.currencyInput = curr.upper()

    def inputCurrCheck(self):
        '''
        compare input currency /w list of possible currencies
        '''
        if self.currencyInput not in self.currencyDict:
            print(f"Ur short currency name - {self.currencyInput} is not matched with default dict, make sure you write it right."
                  f"\nPossible short names:")
            print('"'+'", "'.join([x for x in self.currencyDict.keys()])+'"')
            raise NameError('Wrong currency')
        else:
            return self.currencyDict[self.currencyInput][-1]

    def twoDays(self)-> [dict,int]:
        '''
        return official rate for two last actual dates and min volume of currency rate
        '''
        volume = self.inputCurrCheck()

        resDict = {self.currencyInput:{'temp':None}}

        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(options=options)

        driver.get(self.url)
        htmlVar = driver.page_source

        dateValue = htmlVar\
            .split('<button class="datepicker-filter_button" type="button">')[1]\
            .split('</button>')[0]

        for i in range(2):
            dateValue = DateFiner.dashToDot(datetime.strptime(dateValue, '%d.%m.%Y')-timedelta(days = i), 'dd.mm.yyyy')
            driver.get(self.url + dateValue)
            htmlVar = driver.page_source

            sellValue = CurrencyFiner.toFloat(re.findall(r'\d+,\d+', htmlVar.split(self.currencyInput)[1].split('</td>')[3])[0])

            resDict[self.currencyInput][DateFiner.dotToDash(dateValue)] = sellValue

        del resDict[self.currencyInput]['temp']
        return [resDict, volume]

    def oneDay(self)->[dict,int]:
        '''
        return actual day info and min volume of currency rate
        '''
        oneDayDict = self.twoDays()[0]
        volumeCurrency = self.twoDays()[1]

        del oneDayDict[self.currencyInput][min(oneDayDict[self.currencyInput].keys())]
        return [oneDayDict, volumeCurrency]

class SolibBank:
    '''
    todo:
    словарь городов
    пересечение в валюте(?)

    '''

    currencyDict = {
        'EUR': ['Euro', 1],
        'USD':['US Dollar',1],'JPY':['Japanese Yen',100],'CNY':['Chinese Yuan',1],'KRW':['South Korean Won',1000],'HKD':['HongKong Dollar',10]
    }

    cityDict = {
        'ХАБАРОВСК':'%D0%A5%D0%90%D0%91%D0%90%D0%A0%D0%9E%D0%92%D0%A1%D0%9A'

    }

    def __init__(self, curr='USD', city = 'Хабаровск'):
            self.currencyInput = curr.upper()
            self.cityInput = city.upper()

    %D5 % E0 % E1 % E0 % F0 % EE % E2 % F1 % EA

    https: // solidbank.ru / api / v1 / currency?action = getdata & city =
    %D0 % A5 % D0 % 90 % D0 % 91 % D0 % 90 % D0 % A0 % D0 % 9E % D0 % 92 % D0 % A1 % D0 % 9(A

    & curname) = GBP & date_from = 24.03
    .2025 & date_to = 25.03
    .2025

    def twoDays(self)->[]:
        curname = self.currencyInput
        url = f'https://solidbank.ru/api/v1/currency?action=getdata&city={self.cityInput}&curname={self.currencyInput}&date_from={}&date_to={}'



    def oneDay(self)->[]:
        pass

'''
print(CentralBankOfTheRF.twoDays.__doc__)
print(CentralBankOfTheRF('VND').twoDays())
print(CentralBankOfTheRF('MDL').oneDay())
'''
print('final;e')

