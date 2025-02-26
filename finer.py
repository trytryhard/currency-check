
def dateFiner(dateVal:str)->str:
    ''' DD.MM.YYYY -> YYYY-MM-DD '''
    dateVal.strip()
    sep = ['.']
    if (dateVal[2] in sep) == False or (dateVal[5] in sep) == False or len(dateVal)!=10: return \
        'Wrong separator position or WrongDatePattern'
    for i in sep:
        if i in dateVal:
            return '-'.join(dateVal.split(i)[::-1])

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

