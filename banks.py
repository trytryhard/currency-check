from selenium import webdriver
from datetime import datetime, timedelta, date
import time
import re

from finer import  DateFiner #dateFiner, currencyFiner, dateATBfiner
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
    actualDate = None
    currencyInput = 'USD'
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

    def inputCurrCheck(self, currencyInput):
        if currencyInput not in self.currencyDict:
            print(f"Ur short currency name - {currencyInput} is not matched with default dict, make sure you write it right."
                  f"\nPossible short names:")
            print('"'+'", "'.join([x for x in self.currencyDict.keys()])+'"')
            return False
        else:
            return True

    def twoDays(self) -> dict:
        resDict = {self.currencyInput:{'temp':None}}

        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        htmlVar = driver.page_source

        dateFiner = DateFiner
        dateValue = htmlVar\
            .split('<button class="datepicker-filter_button" type="button">')[1]\
            .split('</button>')[0]

        #self.actualDate = dateFiner.dotToDashISO(dateValue)
        print(dateValue)

        for i in range(2):
            #driver.get(self.url+ str(datetime.strptime(self.actualDate, '%Y-%m-%d')-timedelta(days = i)).split(' ')[0]) # нужно положить 21.03.2025 !!
            print(self.url + dateFiner.dashToDot(datetime.strptime(dateValue, '%d.%m.%Y')-timedelta(days = i), 'dd.mm.yyyy') )

        # <button class="datepicker-filter_button" type="button">19.03.2025</button>


        del resDict[self.currencyInput]['temp']
        pass

qq = CentralBankOfTheRF()
#print(qq.inputCurrCheck(currencyInput='QQQ'))

print(qq.twoDays())
print('final;e')

