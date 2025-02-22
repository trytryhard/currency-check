from main import *

#CBRF
print(parseCbrf(rangeDays=666))
'''
res:  defaultdict(<class 'int'>, {"0_курс{'2025-02-18'}": 91.4347})
'''

print(parseCbrf(rangeDays=2))
'''
res:  defaultdict(<class 'int'>, {"0_курс{'2025-02-15'}": 90.3099, "1_курс{'2025-02-18'}": 91.4347})
'''

#dvb
print(parseDvb())
'''
defaultdict(<class 'int'>, {'valid_date': '2025-02-18', 'buy': '92.4', 'sell': '97.4'})
'''

#solidbank
print(parseSolid(66))
'''
{'2025-02-20': ['sellBank=', '96.4', 'buyBank=', '93.1']}
'''

print(parseSolid(2))
'''
{'2025-02-20': ['sellBank=', '96.4', 'buyBank=', '93.1'], '2025-02-19': ['sellBank=', '97.65', 'buyBank=', '94.5']}
'''

#sovkombank
#vtb
#sber