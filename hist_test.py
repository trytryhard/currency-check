from main import *

#CBRF
print(parseCbrf(2))
'''
{'USD': {'2025-02-22': 88.1676, '2025-02-25': 88.2065}}
'''

print(parseCbrf(66))
'''
 {'USD': {'2025-02-25': 88.2065}}
'''

#dvb
print(parseDvb())
'''
{'USD': {'2025-02-25': {'DVB~buy': 87.5, 'DVB~sell': 93.4}}}
'''

#solidbank
print(parseSolid(66))
'''
{'USD': {'2025-02-25': {'SLD~buy': 90.0, 'SLD~sell': 94.3}}}
'''
print(parseSolid(2))
'''
{'USD': {'2025-02-24': {'SLD~buy': 90.7, 'SLD~sell': 94.45}, '2025-02-25': {'SLD~buy': 90.0, 'SLD~sell': 94.3}}}
'''

#sber
print("parseSber()",parseSber(2))
'''parseSber() {'USD': {'2025-03-03': {'Sber~buy': 86.2, 'Sber~sell': 92.0}, '2025-03-04': {'Sber~buy': 84.9, 'Sber~sell': 91.0}}}'''
print("parseSber()",parseSber(66))
'''parseSber() {'USD': {'2025-03-04': {'Sber~buy': 84.9, 'Sber~sell': 91.0}}}'''

#vtb
print("parseVTB()",parseVTB())
'''parseVTB() {'USD': {'2025-03-03': {'VTB~buy': 89.65, 'VTB~sell': 93.65}}}'''

#atb
print("parseATB()",parseATB())
'''
parseATB() {'USD': {'2025-03-11': {'ATB~buy': 84.97, 'ATB~sell': 95.81}}}'''

# total
print(parseData())
'''
  bankName    buy   sell
0      DVB  88.90  91.00
1      SLD  88.95  91.50
2      VTB  87.15  90.75
3      ATB  83.99  95.05
4     Sber  83.70  90.00
'''
