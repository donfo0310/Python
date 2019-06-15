import io
import requests
import pandas as pd
import lib.Util as u
import datetime

def get_csv_file(yyyymmdd):
    """Specify an underscored date as the argument. ex: _20190101 \n
        If blank is specified, the latest data will be getted."""

    # url + filename
    url = 'https://csvex.com/kabu.plus/csv/japan-all-stock-prices/daily/'
    filename = 'japan-all-stock-prices{0}.csv'.format(yyyymmdd)
    url = url + filename

    # download
    with open('api_setting/credentials.txt', mode='r') as f:
        consumer_id = f.readline().strip()
        consumer_pwd = f.readline().strip()
    res = requests.get(url, auth=requests.auth.HTTPBasicAuth(consumer_id, consumer_pwd))

    # check
    if res.status_code == 200:

        # load to dataframe
        df = pd.read_csv(io.BytesIO(res.content), sep=",", encoding="shift-jis")
        df.to_csv('data/' + filename, index=False, encoding='utf_8_sig')    # can open in Excel using BOM

        # upsert to sqlserver
        with open('sql/upsert.sql', mode='r') as f:
            SQL_TEMPLATE = f.read()
        for line in df.values:
            editSql = SQL_TEMPLATE                      # sql template
            for i,col in enumerate(line):
                editSql = editSql.replace('{' + str(i) + '}', str(col))
            u.ExecuteSQLBySQLServer(editSql)            # upsert
        print('Congrats!')

    # log
    now = datetime.datetime.now()
    with open('result.log', mode='a') as f:
        f.write('\n' + now.strftime("%Y/%m/%d %H:%M:%S ") + str(res.status_code))