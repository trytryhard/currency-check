from selenium import webdriver
import re
import time

'''
todo:
1) making list of currencies kinda-json =>
{
unixtime : {BANK1:
                [
                {currency: 'USD',
                nameCurr:'US Dollar',
                volumeOfCurr:1},

                {currency: 'EUR',
                nameCurr:'EURO',
                volumeOfCurr:1}
                ]
, BANK2:[{currency: 'EUR',
                nameCurr:'EURO',
                volumeOfCurr:1}]}
}

функции:
- определения наличия currencyList.[txt/json]
- перезапись-обновление файла по определению разницы текущего timestamp с указанным в json на 600 секунд(десять минут)
- дозапись объектом, если нет такого наименования банка (?)
-
2)
3)
4)

'''

class CurrencyListCBRF: # <div class="table-wrapper"> tbody /tbody
    @staticmethod
    def getData()->dict:
        url = f'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To='
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(options=options)

        driver.get(url)
        htmlVar = driver.page_source

        htmlVar = htmlVar.split('<div class="table-wrapper">')[1].split('tbody')[1].split('/tbody')[0]

        resDict = {'CBRF':[]}

        for row in htmlVar.split('/tr')[1:-1:]:
            shortName = re.findall('[A-Z]{3}',row)[0]
            volume = re.findall('\d+',row)[1]
            longName = ' '.join(re.findall('[А-Яа-я]+',row))
            resDict['CBRF'].append({"currency": shortName,
                "nameCurr":longName,
                "volumeOfCurr":volume})

        return resDict

class CurrencyListSolid:
    @staticmethod
    def getData()->dict:
        url = f'https://solidbank.ru/currency-transactions/?location=%D0%A5%D0%B0%D0%B1%D0%B0%D1%80%D0%BE%D0%B2%D1%81%D0%BA'
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        htmlVar = driver.page_source

        htmlVar = (htmlVar.split('<div class="currency__info currency__block">')[1]\
                   .split('<div class="currency__info currency__block">')[0])

        resDict = {'Solid':[]}
        for row in htmlVar.split('rates__item')[1::]:
            shortName = re.findall('[A-Z]{3}',row)[0]

            try:
                volume = re.findall('\d+',row.split('</span>')[0])[0]
            except:
                volume = 1

            longName = re.findall('[A-Z]{3}',row)[0]

            resDict['Solid'].append({"currency": shortName,
                "nameCurr":longName,
                "volumeOfCurr":volume})

        return resDict

print(CurrencyListSolid.getData())
