class DateFiner:

    '''def __init__(self,inputDate):
        self.dateValue:str = inputDate'''

    @staticmethod
    def dotToDash(dateValue:str,patternOutput:str='yyyy-mm-dd')->str: # final
        dateValue = str(dateValue).strip().split(' ')[0]

        if len(dateValue) != 10: return f'Needed len = 10, but given len = {len(dateValue)}'

        if patternOutput.lower() == 'yyyy-mm-dd':
            if len(dateValue.split('.')[0]) == 4:
                return dateValue.replace('.', '-')
            else:
                return '.'.join(dateValue.split('-')[::-1])

        if patternOutput.lower() == 'dd-mm-yyyy':
            if len(dateValue.split('.')[0]) == 4:
                return '-'.join(dateValue.split('.')[::-1])  # .replace('-', '.')
            else:
                return dateValue.replace('.', '-')
        else:
            raise NameError(f'Wrong patternOutput argument - "{patternOutput}"')

    @staticmethod
    def dashToDot(dateValue:str,patternOutput:str='yyyy.mm.dd')->str: #
        dateValue = str(dateValue).strip().split(' ')[0]

        if len(dateValue) != 10: return f'Needed len = 10, but given len = {len(dateValue)}'

        if patternOutput.lower() == 'yyyy.mm.dd':
            if len(dateValue.split('-')[0]) == 4:
                return dateValue.replace('-','.')
            else:
                return '-'.join(dateValue.split('.')[::-1])

        if patternOutput.lower() == 'dd.mm.yyyy':
            if len(dateValue.split('-')[0]) == 4:
                return '.'.join(dateValue.split('-')[::-1]) #.replace('-', '.')
            else:
                return dateValue.replace('-','.')
        else:
            raise NameError(f'Wrong patternOutput argument - "{patternOutput}"')


class CurrencyFiner:
    '''def __init__(self,inputDate):
        self.currValue:str = inputDate'''

    @staticmethod
    def toFloat(currValue:str)->float:
        currValue.strip()
        if ',' in currValue: return float(currValue.replace(',','.'))
        if '.' in currValue: return float(currValue)
        else:
            raise
    pass



