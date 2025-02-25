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

#sovkombank
#vtb
#sber