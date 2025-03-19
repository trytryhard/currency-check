import re
from datetime import datetime
import time

def dateFiner(dateVal:str,wantedSep = '-')->str:
    ''' DD.MM.YYYY -> YYYY-MM-DD '''
    dateVal.strip()

    if wantedSep == '-':
        if re.findall("\d{13}",dateVal) != []:
            return str(datetime.fromtimestamp(int(re.findall("\d{13}", dateVal)[0][:-3:]))).split()[0]

        sep = ['.']
        if (dateVal[2] in sep) == False or (dateVal[5] in sep) == False or len(dateVal)!=10: return \
            'Wrong separator position or WrongDatePattern'
        for i in sep:
            if i in dateVal:
                return '-'.join(dateVal.split(i)[::-1])
    if wantedSep=='.':
        return dateVal

    else:
        return 'wrong sep'

def currencyFiner(amount:str)->float:
    amount.strip()
    if '.' in amount: #'Xx.yy' -> float(.)
        return float(amount)
    if ',' in amount: # XXX,YYY" -> float(.)
        return float(amount.replace(',','.'))
    try: # xx -> float(xx)
        return float(amount)
    except Exception as err:
        return f'error of amount-pattern / {err}'

    return 'error of amount-pattern'

def dateATBfiner(dateVal:str)->str:
    monthDict = {'января':'01','февраля':'02',
                 'марта':'03','апреля':'04',
                 'мая':'05','июня':'06',
                 'июля':'07','августа':'08',
                 'сентября':'09','октября':'10',
                 'ноября':'11','декабря':'12'}

    res = dateVal.split(r"currency-foot__text")[1].split(r'г.</div>')[0]

    monthDigit = '00'
    for i in monthDict:
        if i in res:
            monthDigit = '-'+monthDict[i]+'-'

    return re.findall('\d{4}',res)[0] + monthDigit + re.findall('\d{2}',res.split(',')[1])[0]

