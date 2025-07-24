from selenium import webdriver
import re
#import xml.etree.ElementTree as ET
import time
import yaml
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
    '''
    Gettin currency dict for CBRF
    '''

    @staticmethod
    def getData()->dict:
        '''get data of currency(shortName), nameCurr(fullName), volumeOfCurr'''

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
            volume = int(re.findall('\d+',row)[1])
            longName = ' '.join(re.findall('[А-Яа-я]+',row))
            resDict['CBRF'].append({"currency": shortName,
                "nameCurr":longName, #.encode('utf-16'),
                "volumeOfCurr":volume})

        return resDict

class CurrencyListSolid:
    '''
    Gettin currency dict for CBRF
    '''
    @staticmethod
    def getData()->dict:
        '''get data of currency(shortName), nameCurr(fullName), volumeOfCurr'''
        url = f'https://solidbank.ru/currency-transactions/?location=%D0%A5%D0%B0%D0%B1%D0%B0%D1%80%D0%BE%D0%B2%D1%81%D0%BA' # "Хабаровск"
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
                volume = int(re.findall('\d+',row.split('</span>')[0])[0])
            except:
                volume = 1

            longName = re.findall('[A-Z]{3}',row)[0]

            resDict['Solid'].append({"currency": shortName,
                "nameCurr":longName,
                "volumeOfCurr":volume})

        return resDict

class WorkWithFile:
    '''
    class of worin with file R/W +check value in yaml
    '''
    def __init__(self,bankShortName):
        self.bankName=bankShortName

    def checkDateOfFile(self):
        '''def return True if current month in currencyList file else False -> update file with bank currencies'''
        pass
        with open('currencylist.yaml','r') as yamlFile:
            dictOutOfYaml = yaml.safe_load(yamlFile)
            return True if time.strftime('%m-%Y') == list(dictOutOfYaml.keys())[0] else False

    def checkBankInFile(self):
        '''def return True if bankName match with banks in currencyList else False -> update file with bank currencies'''
        pass
        with open('currencylist.yaml','r') as yamlFile:
            dictOutOfYaml = yaml.safe_load(yamlFile)
            return True if (self.bankName in list( x[0] for x in  list( list(x.keys()) for x in (dictOutOfYaml[ list(dictOutOfYaml.keys())[0] ]) ))) else False

    def writeFile(self):
        '''def check by funcs checkBankInFile, checkDateOfFile then update currencyList file
        yaml template: Bank -> currency(short english name), description, volume

        need to add: check bank in yaml, if in it then
        '''
        #if self.checkDateOfFile() == self.checkBankInFile() and self.checkBankInFile() == True:
            #print('Same month flag')
            #return True

        #checkin date for
        print('Same month flag') if self.checkDateOfFile() == True else print('Outdated file')

        #needs to check in same month entity of bankName

        resDict = {time.strftime('%m-%Y'):[]}

        resDict[list(resDict.keys())[0]].append(CurrencyListCBRF.getData())
        resDict[list(resDict.keys())[0]].append(CurrencyListSolid.getData())

        #with open('currencylist.yaml', 'w') as yamlFile:
            #yaml.dump(resDict, yamlFile)#, allow_unicode=True)

        filePath = 'currencylist.yaml'
        try:
            with open(filePath, 'w',  encoding='utf-16') as yamlFile:
                yaml.dump(resDict, yamlFile, default_flow_style=False, sort_keys=False,  allow_unicode=True)
            print(f"Dictionary successfully saved to {filePath}")
        except Exception as e:
            print(f"Error occurred while saving YAML file: {e}")

        #return resDict
        return True

print(WorkWithFile('CBRF').writeFile())
#print(CurrencyListCBRF.getData())