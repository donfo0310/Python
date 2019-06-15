import lib.kabuplus as kabuplus
from datetime import datetime

if __name__ == '__main__':
    yyyymmdd = datetime.strftime(datetime.today(), '%Y%m%d')
    kabuplus.get_csv_file('_' + yyyymmdd)
