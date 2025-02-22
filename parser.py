from selenium import webdriver
from collections import defaultdict
from selenium.webdriver.common.by import By

def q():
    print('q')
    return 0

dictOfCurrencies = {'cbrf':'https://www.cbr.ru/key-indicators/',
                    'dvbank':'https://www.dvbank.ru/',
                    'selenium':'https://www.selenium.dev/selenium/web/web-form.html'}
'''
цбр - курс находится в рамках индикаторов
двбанк - курс на главной странице 
сбер - в рамках карты
'''


driver = webdriver.Chrome()
driver.implicitly_wait(0.5)

driver.get(dictOfCurrencies['cbrf'])
#sel =  driver.get(dictOfCurrencies['selenium'])
htmlVar = driver.page_source
#print(htmlVar)
usd = defaultdict(int)
daysList = [htmlVar.split('валюта</td>')[1].split('</td')[0][-10::],
          htmlVar.split('валюта</td>')[1].split('</td')[1][-10::]]

for i in range(len(daysList)):
    try: usd[f'курс_{daysList[i]}'] = float(htmlVar\
                                      .split('Доллар США')[1]\
                                      .split('</td>')[1+i]\
                                      .split('>')[1]\
                                      .replace(',','.'))
    except Exception as error:
        usd[f'курс_{daysList[i]}'] = error





print(usd)
#price_content = driver.find_element(By.CSS_SELECTOR, "div.key-indicator_content offset-md-2").text
#driver.get_attribute('key-indicator_content offset-md-2')
#print(price_content)


driver.quit()