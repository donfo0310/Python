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
    
def ConvertToFormal(yyyymmdd):
    """ yyyymmddからyyyy/mm/ddへ変換 """
    return datetime.strptime(yyyymmdd, '%Y%m%d').strftime('%Y/%m/%d')

def ConvertToYMD(date_formal):
    """ yyyy/mm/ddからyyyymmddへ変換 """
    return datetime.strftime(date_formal, '%Y%m%d')

def CountWorkday(yyyymmdd_st, yyyymmdd_en, workday='1111100'):
    """ stからenの範囲のうちworkdayが1の場所をカウントして返す。
    例えばworkdayの1111100は土日が休みであることを表す"""
    # ex: between 2019/4/6(sat) and 2019/4/30(tue)
    d = (datetime.strptime(yyyymmdd_st, '%Y%m%d'), datetime.strptime(yyyymmdd_en, '%Y%m%d'))
    # retValue: 00
    retValue = workday[d[0].weekday():]
    # range are 25 days
    d_range_cnt = (d[1]-d[0]).days + 1
    # retValue: 00 + (1111100 * multiple)
    multiple = (d_range_cnt - len(retValue)) // 7
    retValue += workday * multiple
    # retValue: 00 + (1111100 * multiple) + 11
    retValue += workday[:(d_range_cnt - len(retValue)) % 7]
    return retValue.count('1')

if __name__ == '__main__':
    print(GetNowYM(),GetAddYM(-1),GetAddYM(1))
    print(ConvertToFormal('20190419'),ConvertToYMD(datetime.today()))
    print(CountWorkday('20190406','20190430'))