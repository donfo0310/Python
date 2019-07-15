"""年月操作系の関数をまとめました"""
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_now_ym():
    """ systemYMを返します """
    ret = datetime.today()
    return datetime.strftime(ret, '%Y%m')

def get_add_ym(i):
    """ systemYMに i を加味した値を返します。\n
    例: 2019年04月を現在として -1: 201903, +1: 201905 """
    ret = datetime.today() + relativedelta(months=i)
    return datetime.strftime(ret, '%Y%m')

def convert_to_formal(yyyymmdd):
    """ yyyymmddからyyyy/mm/ddへ変換 """
    return datetime.strptime(yyyymmdd, '%Y%m%d').strftime('%Y/%m/%d')

def convert_to_ymd(date_formal):
    """ yyyy/mm/ddからyyyymmddへ変換 """
    return datetime.strftime(date_formal, '%Y%m%d')

def count_work_day(yyyymmdd_st, yyyymmdd_en, workday='1111100'):
    """ stからenの範囲のうちworkdayが1の場所をカウントして返す。
    例えばworkdayの1111100は土日が休みであることを表す。
    2019/4/6(土) and 2019/4/30(火) を例に取ったときに、
    A) 最初の端切れ（土-日）
    B) 掛け算でパターン計算できる範囲（月-日）
    C) 最後の端切れ（月-火）
    と3段階で数字の連結を作ると「00 + (1111100 * multiple) + 11」
    """
    day_range = (datetime.strptime(yyyymmdd_st, '%Y%m%d'), datetime.strptime(yyyymmdd_en, '%Y%m%d'))
    # range are 25 days
    day_range_cnt = (day_range[1]-day_range[0]).days + 1
    # A) 00
    conbine = workday[day_range[0].weekday():]
    # B) (1111100 * multiple)
    multiple = (day_range_cnt - len(conbine)) // 7
    conbine += workday * multiple
    # C) 11
    conbine += workday[:(day_range_cnt - len(conbine)) % 7]
    return conbine.count('1')

def is_over_lap(yyyymmdd_sten1sten2):
    """2つの期間が重なり合うかどうかを判定する。例えば号機等の重複判定にも使えます\n
        例：20190401-20190415,20190410-20190430 のように指定します"""
    ymd1 = yyyymmdd_sten1sten2.split(',')[0].split('-')
    ymd2 = yyyymmdd_sten1sten2.split(',')[1].split('-')
    return ymd2[0] <= ymd1[1] and ymd1[0] <= ymd2[1]

if __name__ == '__main__':
    print(get_now_ym(), get_add_ym(-1), get_add_ym(1))
    print(convert_to_formal('20190419'))
    print(convert_to_ymd(datetime.today()))
    print(count_work_day('20190406', '20190430'))
    print(is_over_lap('20190401-20190430,20190410-20190420'))
    print(is_over_lap('20190401-20190415,20190410-20190430'))
    print(is_over_lap('20190410-20190430,20190401-20190415'))
    print(is_over_lap('20190401-20190409,20190410-20190430'))
    print(is_over_lap('20190410-20190430,20190401-20190409'))
