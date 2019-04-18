from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def GetNowYM():
    """ systemYMを返します """
    d = datetime.today()
    return datetime.strftime(d, '%Y%m')

def GetAddYM(i):
    """ systemYMに i を加味した値を返します。\n
    例: 2019年04月を現在として -1: 201903, +1: 201905 """
    d = datetime.today() + relativedelta(months=i)
    return datetime.strftime(d, '%Y%m')
    
if __name__ == '__main__':
    print(GetNowYM())
    print(GetAddYM(-1),GetAddYM(1))