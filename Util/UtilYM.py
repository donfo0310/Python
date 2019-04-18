from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def GetNowYM():
    """ systemYMを返します """
    d = datetime.today()
    return datetime.strftime(d, '%Y%m')

def GetAddYM(i):
    """ systemYMに i を加味した値を返します。
    例:2008年01月を現在として、1と引数指定すると200802, -1と引数指定すると200712 """
    d = datetime.today() + relativedelta(months=i)
    return datetime.strftime(d, '%Y%m')
    
if __name__ == '__main__':
    print(GetNowYM())
    print(GetAddYM(-1),GetAddYM(1))