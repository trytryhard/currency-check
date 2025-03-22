class DateFiner:

    def __init__(self,inputDate):
        self.dateValue = inputDate

    @staticmethod
    def dotToDashISO(dateValue:str,patternOutput:str='yyyy.mm.dd')->str: # final
        dateValue.split(' ')[0].strip()
        if len(dateValue) != 10: return f'Needed len = 10, but given len = {len(dateValue)}'
        if dateValue.split('.')[0]==4:
            return dateValue.replace('.','-')
        else:
            return '-'.join(dateValue.split('.')[::-1])

    @staticmethod
    def dashToDot(dateValue:str,patternOutput:str='yyyy.mm.dd')->str: #
        dateValue = str(dateValue).split(' ')[0]
        dateValue.split(' ')[0].strip()

        if len(dateValue) != 10: return f'Needed len = 10, but given len = {len(dateValue)}'

        print('in func:',dateValue)

        if patternOutput.lower() == 'dd.mm.yyyy':
            if len(dateValue.split('-')[0]) == 4:
                return '.'.join(dateValue.split('-')[::-1]) #.replace('-', '.')
            else:
                return dateValue.replace('-','.')

        if patternOutput.lower() == 'yyyy.mm.dd':
            if len(dateValue.split('-')[0]) == 4:
                return dateValue.replace('-','.')
            else:
                return '-'.join(dateValue.split('.')[::-1])
        else:
            raise NameError(f'Wrong patternOutput argument - "{patternOutput}"')


class CurrencyFiner:
    pass



