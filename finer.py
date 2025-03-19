class DateFiner:
    def dotTodashISO(self,dateValue:str)->str:
        dateValue.strip()
        if len(dateValue) != 10: return f'Needed len = 10, but given len = {len(dateValue)}'
        if dateValue.split('.')[0]==4:
            return dateValue.replace('.','-')
        else:
            return '-'.join(dateValue.split('.')[::-1])





class CurrencyFiner:
    pass