import pandas as pd
from parser import parseDvb, parseSolid, parseVTB, parseATB, parseSber


def getActualPdFrame(res_dict:dict)->pd.DataFrame:
    argDict = res_dict[list(res_dict.keys())[0]][max(res_dict[list(res_dict.keys())[0]])]

    dataDict = dict()
    dataDict['bankName'] = list(argDict.keys())[0].split('~')[0]

    for i in argDict:
        dataDict[i.split('~')[1]] = [argDict[i]]
    df = pd.DataFrame.from_dict(dataDict)
    return df



def parseData() -> pd.DataFrame:
    resDf = pd.DataFrame()
    errLog = ''
    # outputxlsx = pd.concat([outputxlsx, df], ignore_index=True)
    try:
        print('\r','workin on parseDvb', end='')
        resDf = pd.concat([resDf, getActualPdFrame(parseDvb())], ignore_index=True)
    except Exception as e:
        errLog += 'parseDvb got wrong:'+str(e)+'\r\n'
    try:
        print('\r','workin on parseSolid', end='')
        resDf = pd.concat([resDf, getActualPdFrame(parseSolid(rangeDays=1))], ignore_index=True)
    except Exception as e:
        errLog += 'parseSolid got wrong:'+str(e)+'\r\n'
        #print('parseSolid get wrong:', e)
    try:
        print('\r','workin on parseVTB', end='')
        resDf = pd.concat([resDf, getActualPdFrame(parseVTB())], ignore_index=True)
    except Exception as e:
        errLog += 'parseVTB got wrong:'+str(e)+'\r\n'
        #print('parseVTB get wrong:', e)
    try:
        print('\r','workin on parseATB', end='')
        resDf = pd.concat([resDf, getActualPdFrame(parseATB())], ignore_index=True)
    except Exception as e:
        errLog += 'parseATB got wrong:'+str(e)+'\r\n'
        #print('parseATB get wrong:', e)
    try:
        print('\r','workin on parseSber', end='')
        resDf = pd.concat([resDf, getActualPdFrame(parseSber(rangeDays=1))], ignore_index=True)
    except Exception as e:
        errLog += 'parseSber got wrong:'+str(e)+'\r\n'
        #print('parseSber get wrong:', e)

    print('\r', 'errLog:\n', errLog )

    return resDf.sort_values(by=['sell'],ascending=True, ignore_index=True)


print(parseData())


